from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class EmailVerification(UserBase):
    confirmation_code: str = Field(..., description="Confirmation code for verification")

class UserLogin(UserBase):
    password: str


class ForgotPassword(UserBase):
    confirmation_code: str = Field(..., description="Confirmation code for verification")
    new_password: str = Field(..., description="New password for the user")

class LogOut(BaseModel):
    token: str = Field(..., description="Token to be revoked")