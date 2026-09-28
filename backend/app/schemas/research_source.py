from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearchSourceResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    project_id: int
    title: str
    url: str
    snippet: str
    content: str
    author: str
    published_at: str
    created_at: datetime