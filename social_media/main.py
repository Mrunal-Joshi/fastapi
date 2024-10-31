"""
apis for social media
"""

from social_media.constants import posts
from social_media.posts_model import Posts
from social_media.utilities import find_post

from fastapi import FastAPI
from fastapi.params import Body
from random import randint


app = FastAPI()


@app.get("/")
def getposts():
    return posts


@app.get("/posts/{id}")
def get_post(id: int):
    return find_post(posts, id)


@app.post("/posts")
def create_posts(post: Posts):
    new_post = post.dict()
    new_post["id"] = randint(0, 10000000)
    posts.append(new_post)
    return {"message": "Post created", "post": new_post}


@app.put("/update/{id}")
def update_post(id: int, post_to_update: dict):
    post = find_post(posts, id)

    if post:
        post_to_update["id"] = id
        posts.append(post_to_update)
        posts.remove(post)
        return {"message": "Post Updated", "post": post_to_update}


@app.delete("/delete/{id}")
def delete_post(id: int):
    post = find_post(posts, id)
    posts.remove(post)
    return {"message": "Post Deleted", "deleted post": post, "posts": posts}
