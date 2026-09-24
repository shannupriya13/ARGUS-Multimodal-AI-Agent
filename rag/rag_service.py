from ai.gemini_service import ask_gemini
from rag.vector_store import load_vector_store, search_vector_store


def answer_from_document(
    question: str,
    vector_store_path: str,
    top_k: int = 3
):
    vector_store = load_vector_store(vector_store_path)

    results = search_vector_store(
        question,
        vector_store,
        top_k=top_k
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
You are ARGUS, a helpful AI assistant.

Answer the user's question using the provided document context.

Rules:
- Use the context as the primary source.
- Do not invent information that is not supported by the context.
- If the context does not contain enough information, clearly say so.
- Give a clear and concise answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    answer = ask_gemini(prompt)

    return {
        "answer": answer,
        "sources": results
    }