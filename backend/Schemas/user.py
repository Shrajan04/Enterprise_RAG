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