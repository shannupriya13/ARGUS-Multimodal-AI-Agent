from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import shutil
import os

from ai.gemini_service import ask_gemini
from ai.gemini_multimodal import analyze_image
from ai.agent import classify_input, run_agent
from ai.memory import add_message, clear_history
from rag.rag_service import answer_from_document
from rag.document_processor import process_document


app = FastAPI(
    title="ARGUS",
    description="Multimodal AI Agent",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    prompt: str


class DocumentQuestion(BaseModel):
    question: str


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():
    return {
        "project": "ARGUS",
        "status": "online"
    }


# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================================
# CLEAR MEMORY
# ==========================================================

@app.post("/clear-memory")
def clear_memory():

    clear_history()

    return {
        "success": True,
        "message": "Conversation memory cleared."
    }


# ==========================================================
# TEXT
# ==========================================================

@app.post("/ask")
def ask(request: QueryRequest):

    category = classify_input(request.prompt)

    if category == "TEXT":

        answer = ask_gemini(request.prompt)

        return {
            "success": True,
            "category": "TEXT",
            "response": answer
        }

    return {
        "success": True,
        "category": category,
        "response": f"ARGUS routed this request to: {category}"
    }


# ==========================================================
# IMAGE
# ==========================================================

@app.post("/analyze-image")
def analyze_uploaded_image(
    file: UploadFile = File(...),
    prompt: str = Form(
        "Analyze this image carefully and describe what you see."
    )
):

    image_path = f"temp_{file.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        result = analyze_image(
            image_path,
            prompt
        )

        return {
            "success": True,
            "category": "IMAGE",
            "filename": file.filename,
            "response": result
        }

    finally:

        if os.path.exists(image_path):
            os.remove(image_path)


# ==========================================================
# DOCUMENT QUESTION
# ==========================================================

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
        "category": "DOCUMENT",
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }


# ==========================================================
# DOCUMENT UPLOAD
# ==========================================================

@app.post("/upload-document")
def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    os.makedirs(
        "tests/uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "tests/uploads",
        file.filename
    )

    vector_store_path = os.path.join(
        "tests/uploads",
        "vector_store.json"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        result = process_document(
            file_path,
            vector_store_path
        )

        return {
            "success": True,
            "filename": file.filename,
            "chunks": result["chunks"],
            "vector_store": result["vector_store"]
        }

    except Exception as e:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# AGENT — TEXT / DOCUMENT / TOOL ROUTING
# ==========================================================

@app.post("/agent")
def agent(request: QueryRequest):

    result = run_agent(
        request.prompt
    )

    return {
        "success": True,
        "category": result["category"],
        "response": result["response"],
        "tool": result.get("tool"),
        "sources": result.get("sources")
    }


# ==========================================================
# AGENT — IMAGE ROUTING
# ==========================================================

@app.post("/agent-image")
def agent_image(
    file: UploadFile = File(...),
    prompt: str = Form(
        "Analyze this image carefully and describe what you see."
    )
):

    image_path = f"temp_agent_{file.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        category = "IMAGE"

        result = analyze_image(
            image_path,
            prompt
        )

        # Store image interaction in memory
        add_message(
            "user",
            prompt
        )

        add_message(
            "assistant",
            result
        )

        return {
            "success": True,
            "category": category,
            "filename": file.filename,
            "response": result
        }

    finally:

        if os.path.exists(image_path):
            os.remove(image_path)