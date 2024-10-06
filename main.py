from ast import Import
from passlib.context import CryptContext  # for password hashing
from fastapi import FastAPI, Response, status, HTTPException  # to get response from the server
from fastapi.params import Body     # uvicorn main:app --reload
from pydantic import BaseModel      # uvicorn app.main:app --reload 
from typing import Optional, List  # used to restrict adding unnecessary data from the frontend using post
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

from .routers import post # used to show the col name coz this library only gives values of col not the name of col
from .routers import user, auth, votess
from .import models
from.database import engine

'''
# if dont want to use postman write http://127.0.0.1:8000/docs on google

app = FastAPI()  # instance
models.Base.metadata.create_all(bind = engine) 





# @ is a decorator used to likely enable api for the below defined function
@app.get("/")# '/' = route/ path hai          get  -->  method
async def root():  # can change the name of root  &  remove async
    return {"message": "Hello World"}



@app.post("/createposts")  # Here, data is being sent from the postman(from body section) and is used here. 
def create_posts(payload: dict = Body(...)):  # we r taking the body(postman) & converting into dicty & storing in payload
    print(payload)
    # return{"message":"successfully created posts"}
    return {"new_post":f"title {payload['title']} & content: {payload['content']}"} 



# used to restrict adding unnecessary data from the frontend/postman using received     
class Post(BaseModel):     # Post is a variable   &   BaseModel is from pydantic
    title: str  # it'll chk whether title and content are there of type string
    content: str  # remove content then only title will be printed
    published: bool = True  # True is the default value, if user doesn't provide published
    # rating: Optional[int] = None # None is also a defualt value



#   NOW, USING PYDANTIC TO RESTRICT DATA
#   WE WANT USERS TO SEND ONLY TITLE(str), CONTENT(str)
#   each pydantic model has dict type
@app.post("/createposts2")
def create_posts(post: Post): # Post class where checking will take place& post(var) is the instance to use the class Post
    print(post)  
    print(post.title)
    print(post.dict())  # print the pydantic model as dictionary
    return {"data":f"successfully createposts2 {post}"}    



       
@app.get("/posts")  
def get_posts():
    return {"data":my_posts} # using line 60 to add data
    

@app.post("/posts", status_code=status.HTTP_201_CREATED)  #********** changing status ***********
def create_posts(post: Post): # :post is the class where checking would take place & post = var
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000) # koi bhi no b/w 
    my_posts.append(post_dict)  #my_post me class post ka data bhi add kr diya
    return {"data":my_posts}  # left wala post hai 


my_posts = [{"title": "title of post 1 ", "content": "content of post 1", "id": 1},
            {"title":"favourite food", "content": "i like pizza", "id": 2}]


# this not the best method to grab data from the list, learn new methods later 
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):      ##  DELETE FUNCTION
    for i, p in enumerate(my_posts): # i - index  &  p = refers id 
        if p["id"] == id:
            return i        
        
# # EXTRA
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) -1 ]
#     return {"details": post}


@app.get("/posts/{id}")  # write the id in the http request
def get_posts(id: int, response: Response):  # validate here only that passed param is int then enter
    print(id)
    post = find_post(id)  # no need to write int here
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND # chk status when the respond not found
        # return {"message": f"post with id:{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post_detail": post}
    # return {"post_detail": "this is you f(x) post"}

# When an excepn is raised using raise, it throws the excepn and stops executing further code within  current function.



#  --------------------------------------DELETING A POST------------------------------------------
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has required id
    # my_posts.pop(index)
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"post with id:{id} does not exist or already deleted")
    my_posts.pop(index)
    # return{"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # no data on the terminal





# UPDATE
@app.put("/updatedposts/{id}")
def update(id:int, post:Post):

    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    post_dict = post.dict()
    post_dict[id] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}
#---------------------------------------------------------------------------------------------


# ############################################# CONNECTING TO DATABASE ##################################################
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
                            password = '123456seven',cursor_factory = RealDictCursor) # curso..--> for column names
        cursor = conn.cursor() # cursor -> used to interact with the database, allowing u to execute SQL queries and fetch data
        print("databse connection was successfull!!")
        break
    except Exception as error:
        print("Connecting to database failed & the error is -> ", error)
        time.sleep(2)



@app.get("/sql_get_posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/get_sql_id_posts/{id}")  
def get_posts(id: int):  
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post_detail": post}


# adding new values to the sql database
@app.post("/sql_posts_posts", status_code=status.HTTP_201_CREATED)  #********** changing status ***********
def create_posts(post: Post): # :post is the class where checking would take place & post = var
    cursor.execute("""  INSERT INTO posts (title, content, published) VALUES
                   (%s, %s, %s) RETURNING * """,  # %s is just a string variable where the values are stored like C lang
                    (post.title, post.content, post.published))
    new_posts = cursor.fetchone() # it'll fetch the row one from (RETURNING * ) statement.

    conn.commit() # to save the data in the sql database we use commit
    return {"data":new_posts}  


# DELETE 
@app.delete("/del_sql_posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # no data on the terminal



# UPDATE/replace the existing data
@app.put("/updated_sql_posts/{id}")
def update_post(id:int, post:Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
                   WHERE id = %s
                   returning * """, (post.title, post.content, post.published, str(id),))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")

    return {"data" : updated_post}




# ##########################################        USING ALCHEMY(ORM)      ##############################################

from .database import engine, get_db
from .import models, schema
from sqlalchemy.orm import Session
from fastapi import Depends 
models.Base.metadata.create_all(bind = engine) 


@app.get("/sqlalchemy_get", response_model=List[schema.Post]) # import List
def test_posts(db: Session = Depends(get_db)): # db = variable
    posts = db.query(models.Post).all()        # Post - class name in models file
    
    print(db.query(models.Post))               # Printing the sql query
    
    # return {"data": posts}
    return posts  # automatically converts to dictionary


@app.get("/get_no_sqlalchemy_posts/{id}")  
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post_detail": post}


# adding new values to the sql database                             ***************************
@app.post("/sqlalchemy_posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)  
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)): 

    # new_posts = models.Post(title = post.title, content = post.content,published = post.published)
    # Easy way of this above line when there are many coumns

    new_posts = models.Post(**post.dict()) # unpacking dictionary
    # print(new_posts) # title: Post Title, Content: This is content, Published: True


    # commit
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts) # just like returning * 

    return new_posts



# DELETE
@app.delete("/del_sql_posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# UPDATE/replace the existing data
@app.put("/updated_alchemy_posts/{id}")
def update_post(id:int,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist or already deleted")
    
    post_query.update({'title': "hey this is my updated title", "content": "This is my updated content"}, synchronize_session=False)
    
    db.commit()
    
    return {"data" : "successfull"}




# #########################################################################################################################################################################################

# USERS_INFO Database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")  # password hashin

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)): # everything will be stored in user

    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password


    new_user = models.User(**user.dict())
        
    # commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/get_users_id: /{id}", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def get_user(id:int,db: Session = Depends(get_db) ):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id : {id} does not exist")
    
    return user



'''




app = FastAPI()  # instance
models.Base.metadata.create_all(bind = engine) 



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votess.router)

