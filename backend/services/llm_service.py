# ================================================================
# File: llm_service.py
#
# Purpose:
# Handles communication with the Large Language Model (Gemini).
#
# Responsibilities:
# - Accepts a user question and retrieved document context.
# - Builds a grounded prompt instructing Gemini to answer ONLY
#   from the provided context.
# - Returns Gemini's natural-language answer as a string.
# ================================================================

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",          # gemini-3.7-flash does not exist
    google_api_key=settings.gemini_api_key,
    temperature=0,
)


NOT_FOUND = "I could not find the answer in the provided documents."

def rewrite_question(question: str, history: list) -> str:
    """Turn a follow-up into a standalone question. Unrelated questions are returned unchanged."""
    if not history:
        return question

    convo = "\n".join(f"{m['role']}: {m['text']}" for m in history)
    prompt = f"""
Given the conversation and the latest user message, decide if the message
depends on the earlier conversation (for example "in five points", "explain that",
"what about his education?").

- If it DOES, rewrite it as one complete standalone question.
- If it does NOT, return it exactly as written.

Return ONLY the question, with no explanation.

Conversation:
{convo}

Latest message: {question}

Standalone question:
"""
    try:
        content = llm.invoke(prompt).content
        if isinstance(content, list):
            content = "".join(
                b.get("text", "") if isinstance(b, dict) else str(b) for b in content
            )
        return content.strip() or question
    except Exception:
        return question

def generate_answer(question: str, context: str, history: list | None = None) -> str:
    convo = ""
    if history:
        convo = "Conversation so far (use it ONLY to understand the question, never as a source of facts):\n" + \
                "\n".join(f"{m['role']}: {m['text']}" for m in history)

    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not present in the context, say exactly:
"{NOT_FOUND}"

{convo}

Context:
{context}

Question:
{question}

Answer:
"""
    # ...keep your existing try/except and list-to-string code below this line
    try:
        content = llm.invoke(prompt).content
        if isinstance(content, list):
            content = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        return content.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}"