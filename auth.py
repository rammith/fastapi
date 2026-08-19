import os
from datetime import datetime,timedelta,timezone

from dotenv import load_dotenv
from jose import jwt

from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(username:str):
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub":username,
        "exp":expire
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise credentials_exception
        
        return username
    except jwt.JWTError:
        raise credentials_exception