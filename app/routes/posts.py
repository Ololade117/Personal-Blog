from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.post import Post

router = APIRouter()

@router.get("/")
def home(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.post("/admin/new")
def create_post(
    title: str,
    content: str,
    db: Session = Depends(get_db)
):
    post = Post(
        title = title,
        content=content
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/posts/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    return post