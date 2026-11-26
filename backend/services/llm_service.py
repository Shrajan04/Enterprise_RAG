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

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not present in the context, say exactly:
"{NOT_FOUND}"

Context:
{context}

Question:
{question}

Answer:
"""
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