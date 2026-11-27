import re

# (pattern, reply). Patterns match the WHOLE message, so a real question
# such as "hello world program in the pdf" is never mistaken for small talk.
_RULES = [
    (r"(hi+|he+l+o+|hey+|hola|good (morning|afternoon|evening))",
     "Hello! I can answer questions about the documents you have uploaded. What would you like to know?"),
    (r"(thanks|thank you|thx|ty)",
     "You're welcome! Ask me anything else about your documents."),
    (r"(bye|goodbye|see you)",
     "Goodbye! Come back any time."),
    (r"(who are you|what are you|what can you do|help)",
     "I'm your document assistant. Upload PDFs on the left, then ask me questions. I answer only from your documents and show which file each answer came from."),
    (r"(how are you|how are you doing)",
     "I'm doing well, thanks for asking. What would you like to find in your documents?"),
]


def small_talk_reply(text: str):
    cleaned = re.sub(r"[^\w\s]", "", text.lower()).strip()
    cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
    for pattern, reply in _RULES:
        if re.fullmatch(pattern, cleaned):
            return reply
    return None