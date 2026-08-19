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

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "filename": file.filename,
        "uploaded_by": current_user.email
    } 