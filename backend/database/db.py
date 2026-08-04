# ================================================================
# File: db.py
#
# Purpose:
# Creates and configures the database connection.
#
# Responsibilities:
# - Connects FastAPI with PostgreSQL.
# - Creates the SQLAlchemy Engine.
# - Creates SessionLocal (Session Factory).
# - Creates the Base class for all database models.
#
# This file only sets up the database infrastructure.
# It does NOT perform database queries.
# ================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from sqlalchemy.orm import declarative_base

DATABASE_URL = (
    f"postgresql://{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

