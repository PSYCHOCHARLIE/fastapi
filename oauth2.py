from jose import JWTError, jwt # jwt: provides methods to encode and decode JSON Web Tokens.
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm 
# Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm  # cryptography and hashing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # minutes


def create_access_token(data: dict):
    to_encode = data.copy() # The input data is copied to a new dictionary to_encode. This ensures the original data dictionary is not modified.

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) # adding timedelta (30 min) to current time
    to_encode.update({"exp": expire}) # to_encode.update(): The update -> adds a new key-value pair to the to_encode dicy. The key is "exp" (which stands for "expiration"), and the value is the expiration time (expire), which was calculated in the previous step.

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        id = str(payload.get("user_id")) # str in this context doesn't perform any operations it simply hints developer that the id variable is expected to be a string

        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail =  f"could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)
































# why data.copy is used
# a = {"mango": "haji"}
 
# b = a

# b["apple"]  = "naji"

# print(a)
# print(b)