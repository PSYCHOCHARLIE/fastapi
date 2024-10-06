from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status,Depends, HTTPException, APIRouter
from .. import models, schema, oauth2
from typing import List, Optional
from ..database import get_db # .. 2 step back


router = APIRouter(
    # prefix = "/sqlalchemy_get", # whereever sqlalchemy_get is written remove it coz defines here
    # tags   = ["Posts"]          # name gets change at chrome http://127.0.0.1:8000/docs
)



@router.get("/sqlalchemy_get", response_model=List[schema.Post]) # import List
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()        # Post - class name in models file
    
    print(db.query(models.Post))               # Printing the sql query
    
    # return {"data": posts}
    return posts  # automatically converts to dictionary


@router.get("/get_no_sqlalchemy_posts/{id}")  
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post_detail": post}


# adding new values to the sql database                             ***************************
@router.post("/sqlalchemy_posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)  
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): 
#                                                                     #  this is the thing above that is used to chk the login credentials

    # new_posts = models.Post(title = post.title, content = post.content,published = post.published)
    # Easy way of this above line when there are many coumns

    print(user_id)
    new_posts = models.Post(**post.dict()) # unpacking dictionary
    # print(new_posts) # title: Post Title, Content: This is content, Published: True


    # commit
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts) # just like returning * 

    return new_posts



# DELETE
@router.delete("/del_sql_posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

#    login that if only login person can delete only his post not others
#     if post.owner_id != oauth2.get_current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autorized user")

    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# UPDATE/replace the existing data
@router.put("/updated_alchemy_posts/{id}")
def update_post(id:int,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    
    post_query.update({'title': "hey this is my updated title", "content": "This is my updated content"}, synchronize_session=False)
    
    db.commit()
    
    return {"data" : "successfull"}


@router.get("/sqlalchemy_get_limit", response_model=List[schema.Post]) # import List
def test_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search:Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()        # skip the first 2 post
    # search according to the keyword
    # %20(ascii) means space in url
    
    return posts  # automatically converts to dictionary


