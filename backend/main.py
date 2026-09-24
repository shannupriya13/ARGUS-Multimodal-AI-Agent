from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from ai.gemini_service import ask_gemini
from ai.gemini_multimodal import analyze_image
from rag.rag_service import answer_from_document


app = FastAPI(
    title="ARGUS",
    description="Multimodal AI Agent",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    prompt: str


class DocumentQuestion(BaseModel):
    question: str


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

    try:
        result = analyze_image(image_path, prompt)

        return {
            "success": True,
            "filename": file.filename,
            "response": result
        }

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)


@app.post("/ask-document")
def ask_document(request: DocumentQuestion):
    vector_store_path = "tests/vector_store.json"

    result = answer_from_document(
        request.question,
        vector_store_path,
        top_k=2
    )

    return {
        "success": True,
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }