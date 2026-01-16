from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class ContactCreate(BaseModel):
    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(None, max_length=50) # Optional
    email: EmailStr 
    message: str = Field(..., min_length=10, max_length=1000)


class ContactResponse(BaseModel):
    id:int
    email:EmailStr
    createdAt:datetime
    lastName:Optional[str]
    message:str
    responseMessage:str
    firstName:str
    status:bool

    class config:
        from_attributes=True