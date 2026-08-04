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
from sqlalchemy.orm import Session

from database.dependencies import get_db
from Schemas.user import UserCreate, UserLogin
from config.settings import settings

from models.user import User
from utils.security import hash_password, verify_password

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
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User).filter(User.email == user.email).first()
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
    return {
    "message": "Login successful"
    }