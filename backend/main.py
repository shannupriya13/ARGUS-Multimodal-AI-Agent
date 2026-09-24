from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

from ai.gemini_service import ask_gemini
from ai.gemini_multimodal import analyze_image


app = FastAPI(
    title="ARGUS",
    description="Multimodal AI Agent",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "project": "ARGUS",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QueryRequest):
    answer = ask_gemini(request.prompt)

    return {
        "success": True,
        "response": answer
    }


@app.post("/analyze-image")
def analyze_uploaded_image(
    file: UploadFile = File(...),
    prompt: str = "Analyze this image carefully and describe what you see."
):
    image_path = f"temp_{file.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(image_path, prompt)

    return {
        "success": True,
        "filename": file.filename,
        "response": result
    }