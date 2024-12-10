"""
Data model for posts
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class CreateUser(BaseModel):
    email : EmailStr
    password : str

class DisplayUser(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    # Response will be in sqlalchemy model, hence convert it to pydantic model
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # user_id: int -- whoever is looged in, take that user id

class CreatePost(PostBase):
    pass


#Response Model
class Post(PostBase):
    id : int
    created_at : datetime
    owner : DisplayUser
    # it will tell the pydantic model to read data even if it's not a dict but any obj with attributes
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        from_attributes = True

class Votes(BaseModel):
    post_id : int
    vote_dir : conint(ge=0, le=1)
