# Document Database Model
#
# This module defines the document table used to track uploaded files.
#
# It stores information such as:
# - Which user uploaded the document
# - Original filename
# - File location
# - Upload time
#
# PostgreSQL stores document records, while ChromaDB stores
# the searchable chunks and embeddings.
#==================================================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )