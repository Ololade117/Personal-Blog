from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True)
    content = Column(Text)
    published = Column(Boolean, default=False)