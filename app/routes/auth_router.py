from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import hash_password, verify_password, create_access_token
from app.services.otp_service import create_otp
from app.models import User, OTP
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = User(email=email, hashed_password=hash_password(password), is_verified=False)
    db.add(user)
    db.commit()
    create_otp(db, email)
    return {"message": "User registered. Check email for OTP"}


@router.post("/verify-otp")
def verify_otp(email: str, otp_code: str, db: Session = Depends(get_db)):
    otp_entry = db.query(OTP).filter_by(user_id=email, otp_code=otp_code).first()
    if not otp_entry or otp_entry.expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter_by(email=email).first()
    user.is_verified = True
    db.commit()
    return {"message": "OTP Verified"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """
    Sends an OTP to the user's registered email for password reset.
    """
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    create_otp(db, email)  # Generate and send OTP to email
    return {"message": "OTP sent to registered email"}


@router.post("/reset-password")
def reset_password(email: str, otp_code: str, new_password: str, db: Session = Depends(get_db)):
    """
    Verifies OTP and updates the user's password.
    """
    otp_entry = db.query(OTP).filter_by(user_id=email, otp_code=otp_code).first()

    if not otp_entry or otp_entry.expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)
    db.commit()
    return {"message": "Password reset successfully"}