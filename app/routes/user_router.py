from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import Response
from app.schemas import UserCreate, EmailVerification, UserLogin, ForgotPassword
from app.models import User, OTP

from app.services.user_service import create_user, authenticate_user, reset_user_password, \
    resend_otp, verify_user_email

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup",  response_model = Response)
def register(schema: UserCreate, db: Session = Depends(get_db)):
    return create_user(schema, db)


@router.post("/email-verify",  response_model = Response)
def email_verification(schema: EmailVerification, db: Session = Depends(get_db)):
    return verify_user_email(schema, db)


@router.get("/resend-otp",  response_model = Response)
def resend_verification_code(email: str, db: Session = Depends(get_db)):
    return resend_otp(email, db)

@router.post("/login",  response_model = Response)
def login(schema: UserLogin, db: Session = Depends(get_db)):
    return login_user(schema, db)

@router.post("/logout", response_model = Response)
def logout(token: str, db: Session = Depends(get_db)):
    """
    Logs out the user by invalidating the provided token.
    """
    # Check if the token exists in the database
    token_record = db.query(OTP).filter_by(token=token).first()
    if not token_record:
        raise HTTPException(status_code=404, detail="Token not found")

    # Invalidate the token by deleting it from the database
    db.delete(token_record)
    db.commit()

    return {"message": "Logout successful"}





@router.post("/reset-password",  response_model = Response)
def reset_password(schema: ForgotPassword, db: Session = Depends(get_db)):
    """
    Verifies OTP and updates the user's password.
    """
    return reset_user_password(schema, db)