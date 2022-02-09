from .. import models, schemas, oauth2
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)
   
@router.get("/", response_model=List[schemas.PostOutResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()

    results = db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).all()
    return results

@router.get("/{post_id}", response_model=schemas.PostOutResponse)
def get_post_by_id(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
        status_code=404,
        detail= f"post with id: {post_id} does not exists"
        )
    return post

@router.post("/", response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
        status_code=404,
        detail= f"post with id: {post_id} does not exists"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail= f"Not authorized to perform request action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return f"post with id: {post_id} successfully deleted";


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post1: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
        status_code=404,
        detail= f"post with id: {post_id} does not exists"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail= f"Not authorized to perform request action"
        )

    post_query.update(post1.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()