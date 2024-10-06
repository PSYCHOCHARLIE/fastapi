from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status,Depends, HTTPException, APIRouter
from .. import models, schema
from .. database import get_db # .. 2 step back
from passlib.context import CryptContext  # for password hashing


router = APIRouter(
    # prefix = "/users" ,# whereever sqlalchemy_get is written remove it coz defines here
    # tags   = ["Users"] # name gets change at chrome http://127.0.0.1:8000/docs
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")  # password hashin

@router.post("/users", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)): # everything will be stored in user

    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password


    new_user = models.User(**user.dict())
        
    # commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/get_users_id: /{id}", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def get_user(id:int,db: Session = Depends(get_db) ):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id : {id} does not exist")
    
    return user