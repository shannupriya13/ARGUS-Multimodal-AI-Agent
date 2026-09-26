from ai.gemini_service import ask_gemini
from ai.weather_tool import get_weather
from rag.rag_service import answer_from_document
from ai.memory import add_message, get_history


def classify_input(user_input: str) -> str:

    prompt = f"""
You are the routing brain of ARGUS.

Classify the user's request into exactly one category:

TEXT
IMAGE
DOCUMENT
TOOL

Rules:
- TEXT = normal questions or conversation
- IMAGE = requires analyzing an image
- DOCUMENT = requires information from an uploaded document
- TOOL = requires external information or an external action

Return ONLY the category name.

User request:
{user_input}
"""

    result = ask_gemini(prompt)

    return result.strip().upper()


def run_agent(user_input: str) -> dict:

    category = classify_input(user_input)

    # TEXT + MEMORY
    if category == "TEXT":

        history = get_history()

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

        prompt = f"""
You are ARGUS, a helpful AI assistant.

Conversation history:
{history_text}

Current user message:
{user_input}

Answer the current message using the conversation history when relevant.
Do not mention the internal memory system.
"""

        answer = ask_gemini(prompt)

        add_message("user", user_input)
        add_message("assistant", answer)

        return {
            "category": "TEXT",
            "response": answer
        }

    # TOOL + WEATHER
    if category == "TOOL":

        extraction_prompt = f"""
Extract the city name from the user's request.

Return ONLY the city name.

If no city is mentioned, return:
Vijayawada

User request:
{user_input}
"""

        city = ask_gemini(extraction_prompt).strip()

        weather = get_weather(city)

        add_message("user", user_input)
        add_message("assistant", weather)

        return {
            "category": "TOOL",
            "tool": "weather",
            "response": weather
        }

    # IMAGE
    if category == "IMAGE":

        return {
            "category": "IMAGE",
            "response": "This request requires image analysis."
        }

    # DOCUMENT
    if category == "DOCUMENT":

        vector_store_path = "tests/uploads/vector_store.json"

        result = answer_from_document(
            user_input,
            vector_store_path,
            top_k=2
        )

        answer = result["answer"]

        add_message("user", user_input)
        add_message("assistant", answer)

        return {
            "category": "DOCUMENT",
            "response": answer,
            "sources": result["sources"]
        }

    # UNKNOWN
    return {
        "category": "UNKNOWN",
        "response": "ARGUS could not determine the appropriate route."
    }