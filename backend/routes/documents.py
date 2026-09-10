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

from services.vector_store import add_documents

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    add_documents(
        chunks=chunks,
        embeddings=embeddings,
        user_id= current_user.id,
        filename=file.filename
    )

    return {
        "message": "File uploaded and text extracted successfully",
        "filename": file.filename,
        "uploaded_by": current_user.email,
        "number_of_chunks": len(chunks)
    }
