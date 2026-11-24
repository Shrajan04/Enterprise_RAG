from database.db import Base, engine

from models.document import Document

# Import all models
from models.user import User

Base.metadata.create_all(bind=engine)