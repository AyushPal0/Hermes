from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.research_project import ResearchProject
from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectResponse,
)


router = APIRouter(
    prefix="/api/research",
    tags=["Research"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=ResearchProjectResponse,
)
def create_research_project(
    project: ResearchProjectCreate,
    db: Session = Depends(get_db),
):
    research_project = ResearchProject(
        title=project.title,
        question=project.question,
        depth=project.depth,
        sources=project.sources,
    )

    db.add(research_project)
    db.commit()
    db.refresh(research_project)

    return research_project


@router.get(
    "/",
    response_model=list[ResearchProjectResponse],
)
def get_research_projects(
    db: Session = Depends(get_db),
):
    return (
        db.query(ResearchProject)
        .order_by(ResearchProject.created_at.desc())
        .all()
    )