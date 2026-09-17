from fastapi import FastAPI

app = FastAPI(
    title="AI Researcher API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "AI Researcher API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}