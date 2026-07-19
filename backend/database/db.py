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

