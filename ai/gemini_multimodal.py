from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client()


def analyze_image(image_path: str, prompt: str) -> str:
    image = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            image,
            prompt
        ]
    )

    return response.text