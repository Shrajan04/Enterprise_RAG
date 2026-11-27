# Chat and Retrieval Routes
#
# Accepts questions from authenticated users, rewrites follow-ups into
# standalone questions using recent chat history, retrieves matching chunks
# for that user only, and generates a grounded answer with sources.
#=============================================================================

import json

from fastapi import APIRouter, Depends

from models.user import User
from utils.auth import get_current_user

from services.embedding_service import create_query_embedding
from services.vector_store import search_documents
from services.llm_service import generate_answer, rewrite_question, NOT_FOUND

from services.smalltalk import small_talk_reply

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get("/search")
def search(
    query: str,
    history: str = "[]",
    current_user: User = Depends(get_current_user)
):
    reply = small_talk_reply(query)
    if reply:
        return {"query": query, "answer": reply, "sources": []}

    # History arrives as a JSON string: [{"role": "user", "text": "..."}, ...]
    try:
        history_list = json.loads(history)[-6:]
    except Exception:
        history_list = []

    standalone = rewrite_question(query, history_list)

    query_embedding = create_query_embedding(standalone)

    results = search_documents(
        query_embedding=query_embedding,
        user_id=current_user.id,
        top_k=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    print("STANDALONE:", standalone)
    print("CHUNKS:", [d[:80] for d in documents])

    if not documents:
        return {
            "query": query,
            "answer": "I couldn't find anything relevant in your documents. Upload a document first.",
            "sources": []
        }

    context = "\n\n".join(documents)
    answer = generate_answer(question=standalone, context=context, history=history_list)

    if NOT_FOUND in answer:
        return {"query": query, "answer": answer, "sources": []}

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