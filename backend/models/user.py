# ================================================================
# File: user.py
#
# Purpose:
# Defines the User database table using SQLAlchemy ORM.
#
# Responsibilities:
# - Represents the 'users' table in PostgreSQL.
# - Defines database columns and their data types.
# - Maps Python objects to database records.
#
# Used For:
# Create, Read, Update and Delete (CRUD) operations.
# ================================================================

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())