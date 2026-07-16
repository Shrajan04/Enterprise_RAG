from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings


DATABASE_URL = (
    f"postgresql://{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(DATABASE_URL)
