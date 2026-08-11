# ================================================================
# File: auth.py
#
# Purpose:
# Handles authentication and authorization for protected APIs.
#
# Responsibilities:
# - Extract JWT tokens from incoming requests.
# - Verify JWT signatures and expiration.
# - Identify the authenticated user.
# - Provide reusable authentication dependencies.
#
# Used by:
# Protected API endpoints such as document upload, chat, etc.
# ================================================================



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.user import User
from utils.jwt_handler import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
