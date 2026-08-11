# ================================================================
# File: user.py (schemas)
#
# Purpose:
# Defines request and response schemas using Pydantic.
#
# Responsibilities:
# - Validates incoming client data.
# - Ensures correct data types.
# - Prevents invalid data from reaching the database.
# - Defines what data is returned to the client.
#
# Difference:
# Models  -> Database Structure
# Schemas -> API Request & Response Validation
# ================================================================

from pydantic import BaseModel, EmailStr

#to create user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#to send response to the user
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str