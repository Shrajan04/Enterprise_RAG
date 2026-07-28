from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.user import UserCreate
from config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)
