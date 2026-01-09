from sqlalchemy import Boolean, Integer, Column, DateTime, String, Text
from app.core.database import Base
from sqlalchemy.sql import func

class Contact(Base):
    __tablename__ = "contacts" 
    
    id = Column(Integer, index=True, primary_key=True)
    email = Column(String(255), index=True, nullable=False) 
    firstName = Column(String(100), index=True, nullable=False)
    lastName = Column(String(100))
    message = Column(Text, nullable=False) 
    createdAt = Column(DateTime(timezone=True), server_default=func.now())