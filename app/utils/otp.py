import random
from datetime import datetime ,timedelta

def random_otp():
    return str(random.randint(100000, 999999))

def get_otp_expiry():
    return datetime.utcnow() + timedelta(minutes=5)