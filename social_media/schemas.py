"""
Data model for posts
"""

from pydantic import BaseModel, EmailStr


class Posts(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Posts):
    pass

class CreateUser(BaseModel):
    email : EmailStr
    password : str