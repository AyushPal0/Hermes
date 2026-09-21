from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearchProjectCreate(BaseModel):
    title: str
    question: str
    depth: str = "deep"
    sources: str = "web"


class ResearchProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    question: str
    depth: str
    sources: str
    status: str
    created_at: datetime
    updated_at: datetime