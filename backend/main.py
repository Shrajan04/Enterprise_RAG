from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from Schemas.user import UserCreate
from config.settings import settings

from models.user import User
from utils.security import hash_password

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
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