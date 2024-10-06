from fastapi import FastAPI, Response, status, HTTPException  # to get response from the server
from fastapi.params import Body     # used for post operation
from pydantic import BaseModel # 'pydantic' USED TO SHOW HOW THE SCHEMA/STRUCTURE SHOULD LOOK LIKE
from typing import Optional  # used to restrict adding unnecessary data from the frontend using post
from random import randrange # used for creating random number or random integer
import uvicorn    #(FOR JUPYTER)
import asyncio    #  "    "

# OBJECT/INSTANCE OF FAST API IS CREATED
app = FastAPI()

# ***********************************************************************************************

# IF 2 FUNC HAVE SAME URL THEN IT WILL CONSIDER THE FIRST ONE
@app.get("/1")    # "/" - REPRESENTS THE PATH ON THE SEARCH BAR, 'get' - USED TO READ THE DATA
async def first_func():  # 'async' - CAN REMOVE IT 
    return {"message": " HELLO WORLD "} # RETURNING PYTHON DICTIONARY/LIST & STR, INT,ETC


@app.post("/2")
# FROM POSTMAN 'Body' CONVERT DATA INTO 'dict' AND SAVE IN VARIABLE 'payload'
def create_post(payload: dict = Body(...)): 
    print(payload)
    return {"first_post":f"title:{payload['title']} and content: {payload['content']}" }


# -----------------------------------------------------------------------------------------------

# USING 'pydantic' -> 'Basemodel'
class random_name(BaseModel):
    # CHK 'title' & 'content' IN POSTMAN THAT BOTH ARE PRESENT THERE & ARE OF TYPE 'str'
    # BASICALLY CHOOSING WHAT IS COMING FROM THE POSTMAN
    title:str
    content:str
    # 'bool' MEANING IF NO VALUE IS PASSED IN POSTMAN THEN 'published' DEFAULT VALUE IS "True"
    published:bool = True  
    # = 5/'None'  IF THIS IS NOT THERE IN POSTMAN THEN AUTOMATICALLY TAKES 'rating' = 4
    rating: Optional[int] = 4 


@app.post('/pydantic')
def pydantic_chk(data: random_name): # 'data' VAIRABLE IS A 'pydantic' MODEL
    print(data) # PRINT ALL THE DATA
    print(data.title) # PRINT THE SPECIFIC 'title' ONLY
    print(data.published)
    print(data.rating)
    print(data.dict()) # PROPERTY OF 'pydantic' MODEL THAT IT CONVERTS ALL THE DATA INTO DICT..
    return{"data": data} # RETURNS THE 'data' AS THE DICTIONARY FORMAT COZ WE'VE CONVERTED IT
    # return{"correct?": "yes! working correctly"}

# -----------------------------------------------------------------------------------------------

# SAVING INFORMATION TO THE MEMORY/DATABASE JUST LIKE DATAFRAME('pandas')
# HERE USED [{}],  CAN ALSO USE 'my_posts' = {},{}  MTLB LIST KE BINA BHI BHEJ SKTE HAI BAS DICT...
my_posts = [{'title':'title of post 1', 'content':'content of post 1', 'id' : 1 }, 
            {'title': 'favourite foods', 'content': 'I love pizza', 'id' : 2}]

@app.get('/3')
def saving_my_posts():
    return {'data': my_posts}

@app.post('/pydantic_2')
def saving_my_posts2(data: random_name):
    data_dict = data.dict()
    print(data_dict)
    data_dict['id'] = randrange(0, 1000000)
    my_posts.append(data_dict)
    # return {'Information': my_posts}
    return{'Information': data_dict}


# -----------------------------------------------------------------------------------------------

@app.get("/posts/{id}") # USER GONNA PROVIDE THE 'id' (PATH PARAMETER)
def get_specific_post_thru_id(id): # THE ABOVE 'id' THAT USER PROVIDES IS PASSED IN THE FUNCTION
    print(id)
    return {"post_detail": f"This is the {id} you're interested in"}


# -----------------------------------------------------------------------------------------------
my_posts = [{'title':'title of post 1', 'content':'content of post 1', 'id' : 1 }, 
            {'title': 'favourite foods', 'content': 'I love pizza', 'id' : 2}]

# FUNC TO FIND 'my_post' 'id' AND RETURN THE WHOLE DATA OF THAT 'id'
def gives_id_info(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
@app.get('/find_id/{id}')
def find_id(id: int): # THIS MEANS ONLY TAKE 'int' VALUES IN POSTMAN --- THIS IS THE BEST NOT BELOW 
    xxx = gives_id_info(id) # YOU CAN TYPECAST ABOVE OR HERE BY 'gives_id_info(int(id)) 
    return {"Information" : xxx}

# THERE ARE 2 'ids' OF 'my_posts'. BUT, WHAT IF I WRITE 3 OR 4 OR 5, THEN IT SHOULD GIVE THE ERROR
# 404 NOT FOUND.
# @app.get('/find_id/{id}')
# def find_id(id: int, response: Response):  
#     xxx = gives_id_info(id) 
#     if not xxx:  # IF 'id'  WAS NOT FOUND
#           raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, # CHK POSTMAN STATUS
#                               detail=f"post with {id} was not found") # MESSAGE
#     return {"Information" : xxx}


# -----------------------------------------------------------------------------------------------

# HOW TO USE 'status_code' IN NORMAL GET AND POST METHOD.
@app.get('latest', status_code=status.HTTP_201_CREATED)
def get_latest_post():
    var = my_posts[len(my_posts) -1]
    return {'detail': var}

# -----------------------------------------------------------------------------------------------
# DELETING A POST
my_posts = [{'title':'title of post 1', 'content':'content of post 1', 'id' : 1 }, 
            {'title': 'favourite foods', 'content': 'I love pizza', 'id' : 2}]

def find_index_post(id):
    for i, p in enumerate(my_posts): # USED TO ITERATE OVER (list, tuple, string, etc.)
        if p['id'] == id:
            return i
        
@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # FIND THE INDEX IN THE LIST THAT HAS THE REQUIRED 'id'
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None: # IF THE WRITTEN 'id' DOESN'T EXISTS
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with {id} doesn't exist")

    my_posts.pop(index)
    # return {'message': 'post was successfully deleted'} # NO DATA IS SENT BACK LIKE THIS SO
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------------------------
# UPDATE - MAKING CHANGES TO AN EXISTING POST
class random_name(BaseModel):
    title:str
    content:str
    published:bool = True  
    rating: Optional[int] = 4 

def find_index_post(id):
    for i, p in enumerate(my_posts): # USED TO ITERATE OVER (list, tuple, string, etc.)
        if p['id'] == id:
            return i
        
@app.put('/update/{id}')
def update_posts(id: int, updated_post: random_name):

    index = find_index_post(id)

    if index == None: # IF THE WRITTEN 'id' DOESN'T EXISTS
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with {id} doesn't exist")
    post_dict = updated_post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(updated_post)
    return {'data': post_dict}
    # return {"message": "updated post"}

print(my_posts)


    