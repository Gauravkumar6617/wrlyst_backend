from fastapi import APIRouter, BackgroundTasks, status, Depends
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.email_service import conf
from app.core.database import get_db
from app.model.contact import Contact
from app.schema.contact import ContactCreate, ContactResponse

router = APIRouter(prefix="/contact", tags=["query"])


@router.post(
    "/query",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
async def contact(
    payload: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save to DB
    new_contact = Contact(**payload.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    # Email message
    message = MessageSchema(
    subject="Thank you for contacting Wrklyst",
    recipients=[payload.email],
    template_body={
        "firstName": payload.firstName,
        "message_preview": payload.message[:120]
    },
    subtype=MessageType.html
)

    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message,
        message,
        template_name="contact_confirmation.html"
    )

    # Explicit response (important!)
    return {
        "id": new_contact.id,
        "firstName": new_contact.firstName,
        "lastName": new_contact.lastName,
        "email": new_contact.email,
        "message": new_contact.message[:120],
        "responseMessage": "Thank you for contacting us. We will get back to you shortly.",
        "status": True,
        "createdAt": new_contact.createdAt,
    }
