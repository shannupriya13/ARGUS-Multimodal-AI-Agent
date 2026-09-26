from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client()


def analyze_image(image_path: str, prompt: str) -> str:

    image = Image.open(image_path)

    instruction = f"""
You are ARGUS, a multimodal AI agent.

Analyze the provided image and answer the user's question.

USER QUESTION:
{prompt}

IMPORTANT RULES:
- Focus primarily on answering the user's question.
- Use the image as evidence when relevant.
- Do not give a generic image description unless the user asks for one.
- If the answer requires historical, cultural, scientific, or other background knowledge,
  provide that knowledge when appropriate.
- If the image does not provide enough information, clearly state that and answer using
  relevant general knowledge when possible.
- Give a concise, factual answer.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            image,
            instruction
        ]
    )

    return response.text