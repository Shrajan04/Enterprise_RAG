# ================================================================
# File: documents.py
#
# Purpose:
# Contains API endpoints related to document management.
#
# Responsibilities:
# - Accept document uploads from authenticated users.
# - Validate uploaded files.
# - Save documents to the server.
# - Later, trigger document processing for the RAG pipeline.
#
# This keeps document-related APIs separate from authentication
# and application startup logic.
# ================================================================

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from models.user import User
from utils.auth import get_current_user
import os
import shutil

from services.document_processor import extract_text_from_pdf, chunk_text

from services.embedding_service import create_embeddings, create_query_embedding

from services.vector_store import add_documents, delete_document

from models.document import Document

from sqlalchemy.orm import Session

from database.dependencies import get_db
router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = Document(
    filename=file.filename,
    file_path=file_path,
    user_id=current_user.id
)

    db.add(document)
    db.commit()
    db.refresh(document)

    text = extract_text_from_pdf(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    add_documents(
        chunks=chunks,
        embeddings=embeddings,
        user_id= current_user.id,
        filename=file.filename,
        document_id=document.id
    )

    return {
        "message": "File uploaded and text extracted successfully",
        "document_id": document.id,
        "filename": file.filename,
        "uploaded_by": current_user.email,
        "number_of_chunks": len(chunks)
    }

@router.get("/")
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "created_at": d.created_at,
        }
        for d in documents
    ]

@router.delete("/{document_id}")
def delete_document_route(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete chunks from ChromaDB
    delete_document(document_id)

    # Delete physical file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # Delete document record from PostgreSQL
    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }