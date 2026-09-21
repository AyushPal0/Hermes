from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.research import router as research_router
from app.db.base import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Researcher API",
    description="Backend API for the AI Researcher platform.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)

@app.get("/")
async def root():
    return {
        "message": "AI Researcher API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }