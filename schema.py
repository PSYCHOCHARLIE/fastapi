from pydantic import BaseModel,EmailStr, ValidationError      # uvicorn app.main:app --reload 
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    owner_id : int

# Inheriting above class means instances of PostCreate will have the same attributes as PostBase
class PostCreate(PostBase):
    pass

class UserOut(BaseModel): # response model
    id: int
    email: EmailStr
    created_at: datetime


# Response_model: shows what needs to get visible to the user after execution
class Post(BaseModel):
    id : int
    title: str
    content: str
    published: bool
    # created_at: datetime
    owner_id : int
    owner: UserOut

    # This Config class is used to provide configurations to Pydantic.
    class Config:
        from_attributes = True    # from_attributes will tell the Pydantic model to read the data even if it is not a dict

#############################################################################################################################################



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel): # response model
    id: int
    email: EmailStr
    created_at: datetime
     
    class Config:
        from_attributes = True 

#############################################################################################################################################
class UserLogin(BaseModel): # what user is going to provide
    email: EmailStr
    password: str

###############################################################################################
# for token
class Token(BaseModel):
    access_token: str
    token_type  : str

class TokenData(BaseModel):
    id: Optional[str] = None

###############################################################################################

from pydantic.types import conint

class Vote(BaseModel):
    post_id : int
    dir     : int # less than = to 1