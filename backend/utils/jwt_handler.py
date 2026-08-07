# ================================================================
# File: jwt_handler.py
#
# Purpose:
# Handles JSON Web Token (JWT) operations.
#
# Responsibilities:
# - Generate access tokens after successful login.
# - Verify incoming JWT tokens.
# - Decode token payload.
# - Manage authentication for protected routes.
#
# Benefit:
# Separates authentication token logic from password security.
# ================================================================


from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your_super_secret_key_change_this_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt