# Chat and Retrieval Routes
#
# This module handles user queries for the Enterprise RAG system.
#
# Responsibilities:
# - Accept questions from authenticated users.
# - Convert user questions into embeddings.
# - Search the vector database for relevant document chunks.
# - Restrict retrieval to documents belonging to the authenticated user.
# - Later generate AI-powered answers using the retrieved context.
# - Later support chat history, citations, streaming responses,
#   hybrid search, and agentic retrieval.
#=============================================================================


from fastapi import APIRouter, Depends

from models.user import User
from utils.auth import get_current_user

from services.embedding_service import create_query_embedding
from services.vector_store import search_documents
from services.llm_service import generate_answer

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get("/search")
def search(
    query: str,
    current_user: User = Depends(get_current_user)
):
    query_embedding = create_query_embedding(query)

    results = search_documents(
        query_embedding=query_embedding,
        user_id=current_user.id,
        top_k=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        return {
            "query": query,
            "answer": "I couldn't find anything relevant in your documents. Upload a document first.",
            "sources": []
        }

    context = "\n\n".join(documents)
    answer = generate_answer(question=query, context=context)

    sources = []
    seen = set()
    for metadata, text in zip(metadatas, documents):
        doc_id = metadata["document_id"]
        if doc_id in seen:
            continue
        seen.add(doc_id)
        sources.append({
            "document_id": int(doc_id),
            "filename": metadata["filename"],
            "snippet": text[:200]
        })

    return {"query": query, "answer": answer, "sources": sources}