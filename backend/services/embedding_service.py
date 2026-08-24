# ================================================================
# File: embedding_service.py
#
# Purpose:
# Converts document text chunks into numerical vector embeddings.
#
# Responsibilities:
# - Load the embedding model.
# - Convert text into semantic vectors.
# - Provide embeddings for document storage and user queries.
#
# These embeddings will later be stored in ChromaDB for
# semantic search and retrieval.
# ================================================================

from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_embeddings(chunks: list[str]):
    return embeddings_model.embed_documents(chunks)