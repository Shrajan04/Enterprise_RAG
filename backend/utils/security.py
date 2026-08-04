# ================================================================
# File: security.py
#
# Purpose:
# Handles security-related operations.
#
# Responsibilities:
# - Hashes user passwords before storing them.
# - Verifies passwords during login.
# - Prevents storing plain text passwords.
#
# Benefit:
# Improves application security by protecting user credentials.
# ================================================================

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# for hashing the password
def hash_password(password: str)-> str:
    return pwd_context.hash(password)

#for verifying the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)