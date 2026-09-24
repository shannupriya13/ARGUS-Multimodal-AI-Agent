from fastapi import FastAPI

app = FastAPI(
    title="ARGUS",
    description="Multimodal AI Agent",
    version="0.1.0"
)


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