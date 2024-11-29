"""
Data model for posts
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass


#Response Model
class Post(PostBase):
    id : int
    created_at : datetime

    # it will tell the pydantic model to read data even if it's not a dict but any obj with attributes
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    email : EmailStr
    password : str

class DisplayUser(BaseModel):
    id : int
    email : EmailStr

    # Response will be in sqlalchemy model, hence convert it to pydantic model
    class Config:
        from_attributes = True