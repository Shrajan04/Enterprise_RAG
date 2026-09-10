# ================================================================
# File: document_processor.py
#
# Purpose:
# Handles processing of uploaded documents for the RAG pipeline.
#
# Responsibilities:
# - Extract text from PDF documents.
# - Clean and prepare extracted text.
# - Later, split text into chunks.
# - Prepare documents for embedding and vector storage.
#
# This separates document-processing logic from API route logic.
# ================================================================


import pymupdf

from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(file_path: str) -> str:
    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

def chunk_text(text: str) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    return chunks