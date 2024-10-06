from fastapi import Depends,APIRouter, Response, status, HTTPException 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # used to access the form-data in postman
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2



router = APIRouter()

"""
# chk krne ke liye hai ki band us email id ka exist krta hai ya nhi

@router.post("/login1")
def login(user_credentials: schema.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    
    # create a token
    # return token
    return {"token": "example token"}
"""


# generating token
@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})


    return {"access_token" : access_token, "token_type" : "bearer"}
    