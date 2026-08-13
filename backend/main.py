# ================================================================
# File: main.py
#
# Purpose:
# Entry point of the FastAPI application.
#
# Responsibilities:
# - Creates the FastAPI application instance.
# - Registers API endpoints (or routers in larger projects).
# - Receives HTTP requests from the client.
# - Coordinates request handling using schemas, database, and services.
#
# Flow:
# Client --> FastAPI --> Business Logic --> Database --> Response
# ================================================================

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.dependencies import get_db
from Schemas.user import UserCreate, UserLogin
from config.settings import settings

from models.user import User
from utils.security import hash_password, verify_password

from utils.jwt_handler import create_access_token

from utils.auth import get_current_user

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        
         raise HTTPException(
            status_code=400,
            detail="Email already registered"
             )

    existing_username = (
    db.query(User)
    .filter(User.username == user.username)
    .first()
    )

    if existing_username:
        raise HTTPException(
        status_code=400,
        detail="Username already taken"
    )
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "message": "User registered successfully",
    "user_id": new_user.id
    }

@app.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User).filter(User.email == user.username).first()
    )
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
     )
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = create_access_token(
    data={
        "sub": existing_user.email
    }
    )

    return {
    "access_token": token,
    "token_type": "bearer"
    }

@app.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
    ):
    return {
        "username": current_user.username,
        "email": current_user.email
      }