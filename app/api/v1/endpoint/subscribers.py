from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from pathlib import Path
from app.core.email_service import conf
from app.core.database import get_db
from app.model.subscriber import SubscriberList
from app.schema.subscriber import Subscriber, SubscriberResponse

# --- 1. Email Configuration (Move this to your core/config.py later) ---

router = APIRouter(prefix="/users", tags=["subscriber"])

# Fixed: background_tasks must be a parameter in the function, not the decorator
@router.post("/subscriber", response_model=SubscriberResponse)
async def subscribe(
    payload: Subscriber, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # 2. Check if already exists (Search the Model, not the Schema)
    existed_user = db.query(SubscriberList).filter(SubscriberList.email == payload.email).first()
    if existed_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already subscribed"
        )
    
    # 3. Save to Database (Single Save)
    new_sub = SubscriberList(email=payload.email)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # 4. Prepare Email Message
    message = MessageSchema(
        subject="Welcome to Wrklyst!",
        recipients=[payload.email],
        template_body={"email": payload.email}, 
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    
    # 5. Send Email in Background
    # This makes the API response fast while the email sends in the background
    background_tasks.add_task(fm.send_message, message, template_name="subscriber.html")

    return new_sub