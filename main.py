from fastapi import FastAPI 
from app.routes import posts
from fastapi.staticfiles import StaticFiles
from app.templates import templates

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name = "static"
)

app.include_router(posts.router)

@app.get("/health")
def health():
    return {"message": "Personal Blog API is running"}


