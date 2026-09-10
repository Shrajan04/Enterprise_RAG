# ================================================================
# File: vector_store.py
#
# Purpose:
# Handles storage and retrieval of document embeddings using
# ChromaDB.
#
# Responsibilities:
# - Connect to the ChromaDB vector database.
# - Store document chunks and their embeddings.
# - Store metadata associated with each chunk.
# - Later, perform similarity searches for user questions.
#
# This file keeps vector database operations separate from
# document processing and API route logic.
# ================================================================

import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="enterprise_documents"
)

def add_documents(
    chunks: list[str],
    embeddings: list[list[float]],
    user_id: int,
    filename: str
):
    ids = [
        f"{user_id}_{filename}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "user_id": str(user_id),
            "filename": filename
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    def search_documents(
    query_embedding: list[float],
    user_id: int,
    top_k: int = 5
):
     results = collection.query(
     query_embeddings=[query_embedding],
     n_results=top_k,
     where={
        "user_id": str(user_id)
        }
    )

     return results