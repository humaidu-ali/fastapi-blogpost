
from .. import models, schemas, utils
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password from user
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
        status_code=404,
        detail= f"user with id: {user_id} does not exists"
        )

    return user
