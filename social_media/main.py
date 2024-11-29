"""
apis for social media
"""

from random import randint
from fastapi import FastAPI, status, Response, Depends

from social_media.constants import posts
from social_media.schemas import CreatePost, CreateUser
from social_media.utilities import find_post
from . import models
from .database import engine, get_db, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

#This will create tables in database
models.Base.metadata.create_all(bind=engine)

## API'S
@app.get("/")
def getposts(db : Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return {"data" : data}


@app.get("/posts/{path_id}")
def get_post(path_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=path_id).one_or_none()
    #post = find_post(posts, path_id)
    return {"data" : post}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: CreatePost, db : Session = Depends(get_db)):
    # new_post = post.dict()
    # new_post["id"] = randint(0, 10000000)
    # posts.append(new_post)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created", "post": new_post}


@app.put("/posts/{path_id}")
def update_post(path_id: int, post_to_update: CreatePost, db : Session = Depends(get_db)):
    # post = find_post(posts, path_id)

    # post_to_update["id"] = path_id
    # posts.append(post_to_update)
    # posts.remove(post)
    post = db.query(models.Post).filter(models.Post.id == path_id)

    if not post.first():    
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "Does not exist")
    post.update(post_to_update.dict(), synchronize_session=False)
    db.commit()
    return {"message": "Post Updated", "post": post_to_update.dict()}


@app.delete("/posts/{path_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(path_id: int, db : Session = Depends(get_db)):
    # post = find_post(posts, path_id)

    # posts.remove(post)
    #return {"message": "Post Deleted", "deleted post": post, "posts": posts}
    post = db.query(models.Post).filter_by(id=path_id)
    if not post.first():    
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "Does not exist")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#USER APIS
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "USER created", "post": new_user}