import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from backend.models import OTP, User
from backend.utils.email_sender import send_email


def generate_otp():
    """Generates a 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def create_otp(db: Session, email: str):
    otp_code = generate_otp()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=30)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User with this email does not exist")
    otp_entry = OTP(user_id=user.id, otp_code=otp_code, expiry=expiry)

    db.add(otp_entry)
    db.commit()
    print(f"email_opt-1:{otp_code}")
    send_email(email, "Your OTP Code", f"Your OTP is {otp_code}")

def generate_and_store_otp(db: Session, email: str, user_id :str):
    """Creates a new OTP for the user and sends it via email if the user exists."""

    # Remove old OTPs
    db.query(OTP).filter(OTP.user_id == user_id).delete()

    # Generate new OTP and set expiry time (now timezone-aware)
    otp_code = generate_otp()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Create and save OTP entry
    otp_entry = OTP(user_id=user_id, otp_code=otp_code, expiry=expiry)
    db.add(otp_entry)
    db.commit()
    print(f"email_opt-2:{otp_code}")

    # Send OTP email
    send_email(email, "Password Reset OTP", f"Your OTP code is {otp_code}")

def password_reset_otp(db: Session, email: str, user_id):
    # Generate OTP and expiry time
    otp_code = generate_otp()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Store OTP in database
    existing_otp = db.query(OTP).filter(OTP.user_id == user_id).first()
    if existing_otp:
        existing_otp.otp_code = otp_code
        existing_otp.expiry = expiry
    else:
        otp_entry = OTP(user_id=user_id, otp_code=otp_code, expiry=expiry)
        db.add(otp_entry)

    db.commit()
    print("otp", otp_code)
    # Send OTP via email
    subject = "Password Reset OTP"
    body = f"Your OTP for password reset is: {otp_code}. It expires in 10 minutes."
    send_email(email, subject, body)
