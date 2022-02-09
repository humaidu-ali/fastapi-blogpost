from sys import prefix
from .. import models, schemas, oauth2
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db


router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail= f"post with id {vote.post_id} does not exist"
           )

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.vote_dir == 1):
        if found_vote:
            raise HTTPException(
            status_code=409,
            detail= f"user {current_user.id} has already voted on post {vote.post_id}"
           )
           
        new_vote = models.Vote(user_id=current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message" : "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
            status_code=404,
            detail= f"vote does not exist"
           )

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Successfully deleted vote"}


