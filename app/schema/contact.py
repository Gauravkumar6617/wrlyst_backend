from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(None, max_length=50) # Optional
    email: EmailStr # This validates format like 'user@example.com'
    message: str = Field(..., min_length=10, max_length=1000)