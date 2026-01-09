from pydantic import BaseModel ,EmailStr
from datetime import datetime

class Subscriber(BaseModel):
    email:EmailStr


class SubscriberResponse(BaseModel):
    id:int

    email:EmailStr
    createdAt:datetime
    
    class config:
        from_attributes=True
    