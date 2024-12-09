from fastapi import status, Response, Depends
from typing import List, Optional
from .. import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/posts")

@router.get("/", response_model=List[schemas.Post])
def getposts(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
        limit : int = 10, skip : int =0, search : Optional[str] = ""):

    # NOTE - skip/offset will skip first "skip" posts
    data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # .filter(models.Post.owner_id = current_user.id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No posts found")
    return data


@router.get("/{path_id}", response_model=schemas.Post)
def get_post(path_id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter_by(id=path_id).one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "post not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorozed to retrieve post")
    return post


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{path_id}", response_model=schemas.Post)
def update_post(path_id: int, post_to_update: schemas.CreatePost, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == path_id)

    post_query = post.first()
    if not post_query:    
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Does not exist")

    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorozed to perform update")

    post.update(post_to_update.dict(), synchronize_session=False)
    db.commit()
    return post_query


@router.delete("/{path_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(path_id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter_by(id=path_id)

    post_query = post.first()

    if not post_query:    
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Does not exist")

    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorozed to perform delete")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
