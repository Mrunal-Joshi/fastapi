"""
apis for social media
"""

from random import randint
from fastapi import FastAPI, status, Response
import psycopg2
import time
from social_media.constants import posts
from social_media.posts_model import Posts
from social_media.utilities import find_post


app = FastAPI()

import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            database = "fastapi",
            user = "postgres",
            password = "2810",
            host = "localhost",
            port = "5432"
        )  # creates a new database session
        print("CONNECTED SUCCESSFULLY")

        cursor = conn.cursor()  ## alllows interaction with the server
        break
    except:
        print("DB NOT CONNECTED")
        time.sleep(2)
        

@app.get("/")
def getposts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print("POSTS", posts)
    return posts


@app.get("/posts/{path_id}")
def get_post(path_id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,path_id)
    #post = find_post(posts, path_id)
    post = cursor.fetchone()
    return post 


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Posts):
    # new_post = post.dict()
    # new_post["id"] = randint(0, 10000000)
    # posts.append(new_post)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning *""", (post.title, post.content, post.published))
    created_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post created", "post": created_post}


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
