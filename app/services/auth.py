from sqlalchemy.orm import Session
from app.model.users import Users
from app.schema.users import UserCreate
from app.core.security import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    db_user = Users(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
