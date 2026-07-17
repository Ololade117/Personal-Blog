from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.post import Post
from app.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request,
         db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
            "posts": posts,
        },
    )

@router.post("/admin/new", response_class=HTMLResponse)
def create_post(
    title: str = Form(...),
    tag : str = Form(""),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    post = Post(
        title = title,
        tag = tag,
        content=content
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return RedirectResponse(
        url="/",
        status_code=303
    )

@router.get("/posts/{post_id}", response_class=HTMLResponse)
def get_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={
            "request": request,
            "post": post,
        },
    )

@router.get(
    "/admin/new",
    response_class=HTMLResponse
)
def new_post_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={
            "request": request,
        },
    )

@router.get("/admin/edit/{post_id}",
    response_class=HTMLResponse)
def edit_post_page(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "post": post,
        },
    )

@router.post("/admin/edit/{post_id}")
def update_post(
    post_id: int,
    title: str = Form(...),
    tag: str = Form(""),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )
    post.title = title
    post.tag = tag
    post.content = content
    db.commit()
    return RedirectResponse(
        url=f"/posts/{post_id}",
        status_code=303
    )


@router.post("/admin/delete/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )
    db.delete(post)
    db.commit()
    return RedirectResponse(
        url="/",
        status_code=303
    )