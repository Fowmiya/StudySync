from fastapi import FastAPI

app = FastAPI(
    title="StudySync API",
    description="AI-Powered Student Study & Performance Platform",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "StudySync backend is running"
    }