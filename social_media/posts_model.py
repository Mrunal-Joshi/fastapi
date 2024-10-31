"""
Data model for posts
"""

from pydantic import BaseModel


class Posts(BaseModel):
    title: str
    content: str
