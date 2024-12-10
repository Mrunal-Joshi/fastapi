from fastapi import APIRouter, Depends, status, HTTPException
from  sqlalchemy.orm import Session
from .. import database, models, oauth2, schemas


router = APIRouter(prefix = "/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def manage_vote(votes : schemas.Votes, db : Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id, models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()

    if votes.vote_dir == 1: #Add vote
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already Voted!!")
        add_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id)
        db.add(add_vote)
        db.commit()

        return {"message" : "Successfully added vote!!"}
    else:  #Delete Vote
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found!!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Successfully deleted vote!!"}

