from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text