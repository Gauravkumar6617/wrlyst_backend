# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.users import Users
import os

# 1. Define the scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "7d9f6e8a0b1c2d3e4f5g6h7i8j9k0l1m")
ALGORITHM = "HS256"

# 2. Use the scheme
def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme) # <--- This is where it's used
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def verifyadmin(current_users:Users=Depends(get_current_user)):
    if not current_users.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have sufficient permissions to access this resource.")
    return current_users