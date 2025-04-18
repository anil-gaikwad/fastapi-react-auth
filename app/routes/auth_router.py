from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.response import Response
from app.schemas import (
    UserCreate, EmailVerification, UserLogin, ForgotPassword, 
    LogOut, UserBase
)

from app.services.auth_service import (create_user, resend_verification_code,
                                       verify_user_email, update_password_with_otp,
                                       revoke_access_token, login_user, send_password_reset_otp)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/signup", response_model=Response)
def user_register(schema: UserCreate, db: Session = Depends(get_db)):
    return create_user(schema, db)


@auth_router.post("/verify-email", response_model=Response)
def email_verification(schema: EmailVerification, db: Session = Depends(get_db)):
    return verify_user_email(schema, db)


@auth_router.post("/resend-otp", response_model=Response)
def resend_verification(schema: UserBase, db: Session = Depends(get_db)):
    return resend_verification_code(schema.email, db)


@auth_router.post("/forgot-password", response_model=Response)
def reset_password(schema: UserBase, db: Session = Depends(get_db)):
    return send_password_reset_otp(schema.email, db)


@auth_router.post("/reset-password", response_model=Response)
def reset_password(schema: ForgotPassword, db: Session = Depends(get_db)):
    return update_password_with_otp(schema, db)


@auth_router.post("/login", response_model=Response)
def login(schema: UserLogin, db: Session = Depends(get_db)):
    return login_user(schema, db)


@auth_router.post("/logout", response_model=Response)
def logout(schema: LogOut, db: Session = Depends(get_db)):
    return revoke_access_token(schema.token, db)

