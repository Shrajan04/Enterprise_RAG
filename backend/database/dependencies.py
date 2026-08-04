# ================================================================
# File: dependencies.py
#
# Purpose:
# Provides reusable dependencies for FastAPI.
#
# Responsibilities:
# - Creates a new database session for every request.
# - Supplies the session to API endpoints.
# - Automatically closes the session after the request ends.
#
# Benefit:
# Prevents duplicate code and ensures proper database
# connection management.
# ================================================================

from database.db import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()