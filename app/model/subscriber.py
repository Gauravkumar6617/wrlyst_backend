# app/model/subscriber.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class SubscriberList(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # REMOVE the () after utcnow
    createdAt = Column(DateTime, default=datetime.utcnow)