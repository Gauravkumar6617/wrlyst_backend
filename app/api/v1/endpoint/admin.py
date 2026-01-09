from fastapi import APIRouter ,Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.api.deps import get_current_user,verifyadmin
from app.model.users import Users
from app.model.subscriber import SubscriberList

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/get-all-users", dependencies=[Depends(verifyadmin)])
def get_all_users(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 5 # Defaulting to 5 as requested
):
    users = db.query(Users).offset(skip).limit(limit).all()
    total_count = db.query(Users).count()
    
    return {
        "users": users,
        "total": total_count,
        "limit": limit,
        "skip": skip
    }

@router.get("/get-all-subscriber" ,dependencies=[Depends(verifyadmin)])
def getAllSubscriber(db:Session=Depends(get_db),skip:int=0 ,limit:int=5):
 subscribers = db.query(SubscriberList).offset(skip).limit(limit).all()
 return subscribers