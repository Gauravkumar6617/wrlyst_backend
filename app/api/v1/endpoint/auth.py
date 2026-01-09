from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.users import UserCreate, UserLogin, UserResponse ,TokenResponse ,UserOut,verifyOtp ,UsernameUpdate ,ResetPasswordRequest
from app.services.auth import create_user, authenticate_user
from app.core.security import create_access_token
from app.model.users import  Users
from app.core.security import hash_password ,verify_password
from app.services.otp_service import get_Otp ,get_otp_expiry ,check_otp
from app.core.email_service import send_otp_email 
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings
from app.model.users import Users
from app.api.deps import get_current_user
import random
from datetime import datetime, timedelta
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(Users).filter(Users.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email already exist. Try with another one.")
    
    user=Users(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password)
    )
    otp=get_Otp(user)

    db.add(user)
    db.commit()
    print(f"--- REGISTRATION DEBUG ---")
    print(f"Email: {user.email}")
    print(f"OTP Generated & Saved: {otp}")
    print(f"--------------------------")
    db.refresh(user)
    await send_otp_email(user.email ,otp)
    return {"message":"An Otp has been send"}



@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_verified:
        raise HTTPException(403, "Email not verified")
    
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token":access_token,
        "token_type":"bearer",
        "message":"login scucess",
        "user":{
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
            "is_verified": user.is_verified
        }

    }


@router.post("/google-login")
async def google_login(token_data: dict, db: Session = Depends(get_db)):
    token = token_data.get("token")
    try:
        # 1. Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo['email']
        google_id = idinfo['sub']
        name = idinfo.get('name')

        # 2. Check if user exists
        user = db.query(Users).filter(Users.email == email).first()

        if not user:
            # Create new user
            user = Users(
                email=email,
                username=name,
                google_id=google_id,
                auth_provider="google",
                is_verified=True  # Google emails are already verified
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # If user exists but doesn't have a google_id yet, update it
            if not user.google_id:
                user.google_id = google_id
                user.auth_provider = "google"
                db.commit()

        # 3. Generate JWT
        access_token = create_access_token(data={"sub": user.email})
        
        # 4. Return the token AND the username for your Frontend Toast
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "username": user.username  # <--- Crucial for your Next.js toast
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")
    

# Use the Pydantic class 'verifyOtp' as the type, not the function 'check_otp'
@router.post("/verify-otp")
def verify_email(data: verifyOtp, db: Session = Depends(get_db)):
    # 1. Fetch user
    user = db.query(Users).filter(Users.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"DEBUG: User found: {user.email}")
    print(f"DEBUG: OTP in DB: '{user.otp_code}' (Type: {type(user.otp_code)})")
    print(f"DEBUG: OTP from Frontend: '{data.otp}' (Type: {type(data.otp)})")
    # 2. Call the FUNCTION 'check_otp' (make sure this function is imported)
    # Note: Use the function logic here
    if not check_otp(user, data.otp): 
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # 3. Success logic
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}



@router.patch("/update-me")
def UpdateUser(payload:UsernameUpdate,db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):
    current_user.username=payload.username
    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated successfully", "username": current_user.username}

@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        # Security tip: don't reveal if email exists, just say "Sent"
        return {"message": "If this email is registered, an OTP has been sent."}

    # 1. Generate 6-digit OTP
    otp = f"{random.randint(100000, 999999)}"
    
    # 2. Save to DB
    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.commit()


    print("\n" + "="*30)
    print(f"FORGOT PASSWORD REQUEST")
    print(f"User Name: {user.username}")
    print(f"User Email: {user.email}")
    print(f"Generated OTP: {otp}")
    print("="*30 + "\n")
    # 3. Send the Email (reuse your existing email service)
    # await send_otp_email(email, otp) 
    
    return {"message": "OTP sent successfully"}

@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    # 1. Find the user
    user = db.query(Users).filter(Users.email == payload.email).first()

    # 2. Security Check: Does user exist and does OTP match?
    if not user or user.otp_code != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP or Email")

    # 3. Time Check: Has the OTP expired?
    if user.otp_expiry and datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    # 4. Success Path: Hash new password and Update DB
    user.password_hash = hash_password(payload.new_password)
    
    # 5. Cleanup: Clear OTP so it cannot be used again
    user.otp_code = None
    user.otp_expiry = None
    
    db.commit()

    print(f"SUCCESS: Password for {user.username} has been reset.")
    
    return {"message": "Password reset successfully. You can now login with your new password."}