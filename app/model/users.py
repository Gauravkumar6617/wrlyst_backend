from sqlalchemy import Boolean ,Integer , String, DateTime , Column
from sqlalchemy.sql import func
from app.core.database import Base

class Users(Base):
    __tablename__ ="users"

    id=Column(Integer , primary_key=True ,index=True)
    email=Column(String , index=True ,unique=True , nullable=False)
    username=Column(String ,index=True , nullable=False)
    password_hash=Column(String , nullable=True , )
    is_verified=Column( Boolean ,default=False )
    is_admin=Column(Boolean , default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    otp_code=Column(String , nullable=True)
    otp_expiry=Column(DateTime ,nullable=True)
    auth_provider=Column(String , default="local")
    google_id=Column(String ,unique=True ,nullable=True)