"""
apis for social media
"""

from random import randint
from fastapi import FastAPI, status, Response, Depends
from typing import List
from social_media.constants import posts
from social_media.utilities import find_post
from . import models, schemas, utils
from .database import engine, get_db, SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

app = FastAPI()

#This will create tables in database
models.Base.metadata.create_all(bind=engine)



## API'S
@app.get("/posts", response_model=List[schemas.Post])
def getposts(db : Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return data


@app.get("/posts/{path_id}", response_model=schemas.Post)
def get_post(path_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=path_id).one_or_none()
    #post = find_post(posts, path_id)
    return post


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db : Session = Depends(get_db)):
    # new_post = post.dict()
    # new_post["id"] = randint(0, 10000000)
    # posts.append(new_post)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put("/posts/{path_id}", response_model=schemas.Post)
def update_post(path_id: int, post_to_update: schemas.CreatePost, db : Session = Depends(get_db)):
    # post = find_post(posts, path_id)

    # post_to_update["id"] = path_id
    # posts.append(post_to_update)
    # posts.remove(post)
    post = db.query(models.Post).filter(models.Post.id == path_id)

    if not post.first():    
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "Does not exist")
    post.update(post_to_update.dict(), synchronize_session=False)
    db.commit()
    return post_to_update.dict()


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
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # hash the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/user/{id}", response_model=schemas.DisplayUser)
def get_user(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User does not exit")
    return user
