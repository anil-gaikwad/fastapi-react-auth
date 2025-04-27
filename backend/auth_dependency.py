from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from backend.database import get_db
from backend.models import User
from backend.security import SECRET_KEY, ALGORITHM
from backend.utils.util import HTTPResponse

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode JWT token and return the current authenticated user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return HTTPResponse(status_code=401, message="Invalid authentication token").return_response()
    except jwt.ExpiredSignatureError:
        return HTTPResponse(status_code=401, message="Token has expired").return_response()
    except InvalidTokenError:
        return HTTPResponse(status_code=401, message="Invalid authentication token").return_response()

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return HTTPResponse(status_code=401, message="User not found").return_response()
    return user
