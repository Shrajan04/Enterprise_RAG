from database.db import Base, engine

# Import all models
from models.user import User

Base.metadata.create_all(bind=engine)