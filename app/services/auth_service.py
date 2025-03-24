from datetime import datetime, timezone, timedelta

from fastapi import HTTPException

from app.models import User, OTP, RevokedToken
from app.security import hash_password, verify_password, create_access_token, decode_access_token
from app.services.otp_service import generate_and_store_otp, create_otp, password_reset_otp
from app.utils.util import response


def create_user(payload, db):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password), is_verified=False)
    db.add(user)
    db.commit()
    create_otp(db, payload.email)
    return {"message": "User registered. Check email for OTP"}


def verify_user_email(payload, db):

    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_entry = db.query(OTP).filter_by(user_id=user.id).first()
    if not otp_entry:
        raise HTTPException(status_code=400, detail="OTP not found")

    if otp_entry.expiry.tzinfo is None:
        otp_entry.expiry = otp_entry.expiry.replace(tzinfo=timezone.utc)

    if otp_entry.expiry < datetime.now(timezone.utc):
        db.delete(otp_entry)  # Delete expired OTP
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    user = db.query(User).filter_by(email=payload.email).first()
    user.is_verified = True
    db.commit()

    return {"message": "OTP Verified"}


def resend_verification_code(email, db):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    generate_and_store_otp(db, email, user.id)
    return {"message": "OTP resent successfully"}


def send_password_reset_otp(email, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    password_reset_otp(db, email,  user.id)

    return {"message": "OTP sent to your email"}

def update_password_with_otp(payload, db):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_entry = db.query(OTP).filter_by(user_id=user.id, otp_code=payload.confirmation_code).first()
    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expiry.tzinfo is None:
        otp_entry.expiry = otp_entry.expiry.replace(tzinfo=timezone.utc)

    if otp_entry.expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.hashed_password = hash_password(payload.new_password)
    db.commit()

    return {"message": "Password reset successfully"}

def login_user(payload, db):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


def revoke_access_token(token, db):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if token is already revoked
    if db.query(RevokedToken).filter_by(token=token).first():
        raise HTTPException(status_code=400, detail="Token already revoked")

    # Add the token to revoked tokens
    revoked_token = RevokedToken(token=token)
    db.add(revoked_token)
    db.commit()

    return {"message": "Logout successful. Token has been blacklisted."}
