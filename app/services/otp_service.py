from datetime import datetime ,timezone
from app.utils.otp import get_otp_expiry, random_otp

def get_Otp(user):
    otp = random_otp()
    user.otp_code = otp  # Changed from emailOtp to otp_code
    user.otp_expiry = get_otp_expiry()
    return otp

def check_otp(user, otp: str):
    # Changed from emailOtp to otp_code
    if not user.otp_code:
        print("DEBUG: No OTP found in database for this user")
        return False
    
    now = datetime.now(timezone.utc) if user.otp_expiry.tzinfo else datetime.utcnow()
    
    if user.otp_expiry < now:
        print("DEBUG: OTP has expired")
        return False
        
    return str(user.otp_code) == str(otp)

