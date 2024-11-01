"""
apis for social media
"""

from random import randint
from fastapi import FastAPI, status, Response

from social_media.constants import posts
from social_media.posts_model import Posts
from social_media.utilities import find_post


app = FastAPI()


@app.get("/")
def getposts():
    return posts


@app.get("/posts/{path_id}")
def get_post(path_id: int):
    post = find_post(posts, path_id)
    return post


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Posts):
    new_post = post.dict()
    new_post["id"] = randint(0, 10000000)
    posts.append(new_post)
    return {"message": "Post created", "post": new_post}


@app.put("/posts/{path_id}")
def update_post(path_id: int, post_to_update: dict):
    post = find_post(posts, path_id)

    post_to_update["id"] = path_id
    posts.append(post_to_update)
    posts.remove(post)
    return {"message": "Post Updated", "post": post_to_update}


@app.delete("/posts/{path_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(path_id: int):
    post = find_post(posts, path_id)

    posts.remove(post)
    #return {"message": "Post Deleted", "deleted post": post, "posts": posts}
    return Response(status_code = status.HTTP_204_NO_CONTENT)
