from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    username: str = Field(..., description="User's name")

class EmailVerification(UserBase):
    confirmation_code: str = Field(..., description="Confirmation code for verification")

class UserLogin(UserBase):
    password: str


class ForgotPassword(UserBase):
    confirmation_code: str = Field(..., description="Confirmation code for verification")
    new_password: str = Field(..., description="New password for the user")

class LogOut(BaseModel):
    token: str = Field(..., description="Token to be revoked")

# New schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_verified: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None