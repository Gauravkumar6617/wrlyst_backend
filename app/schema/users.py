from pydantic import BaseModel, EmailStr
from datetime import datetime


# ---------- SIGNUP ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

#-------UserOut--------------

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_verified: bool
    created_at: datetime 


#--------verifyotp--------
 
class verifyOtp(BaseModel):
    email:EmailStr
    otp:str

    class Config:
        from_attributes = True

        
# ---------- LOGIN ----------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user:UserOut
