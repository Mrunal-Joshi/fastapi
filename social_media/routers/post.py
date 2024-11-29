from fastapi import status, Response, Depends
from typing import List
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/posts")

@router.get("/", response_model=List[schemas.Post])
def getposts(db : Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return data


@router.get("/{path_id}", response_model=schemas.Post)
def get_post(path_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=path_id).one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "post not found")
    return post


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db : Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{path_id}", response_model=schemas.Post)
def update_post(path_id: int, post_to_update: schemas.CreatePost, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == path_id)

    post_query = post.first()
    if not post_query:    
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "Does not exist")

    post.update(post_to_update.dict(), synchronize_session=False)
    db.commit()
    return post_query


@router.delete("/{path_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(path_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=path_id)
    if not post.first():    
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "Does not exist")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
