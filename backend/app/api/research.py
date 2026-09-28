from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.research_project import ResearchProject
from app.models.research_source import ResearchSource
from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectResponse,
)
from app.schemas.research_source import ResearchSourceResponse
from app.services.research_pipeline import ResearchPipeline
from pydantic import BaseModel

from app.services.vector.chroma_store import ChromaStore

class ResearchQuery(BaseModel):
    query: str
    n_results: int = 5

router = APIRouter(
    prefix="/api/research",
    tags=["Research"],
)


# ---------------------------------------------------------
# DATABASE DEPENDENCY
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# CREATE RESEARCH PROJECT
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# GET ALL RESEARCH PROJECTS
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[ResearchProjectResponse],
)
def get_research_projects(
    db: Session = Depends(get_db),
):
    return (
        db.query(ResearchProject)
        .order_by(
            ResearchProject.created_at.desc()
        )
        .all()
    )


# ---------------------------------------------------------
# RUN RESEARCH
# ---------------------------------------------------------

@router.post("/{project_id}/run")
async def run_research(
    project_id: int,
    db: Session = Depends(get_db),
):
    # Find the research project
    project = db.get(
        ResearchProject,
        project_id,
    )

    # Project doesn't exist
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Research project not found",
        )

    # Mark project as currently researching
    project.status = "researching"

    db.commit()

    # Create the research pipeline
    pipeline = ResearchPipeline(db)

    try:
        # Run web search + webpage extraction
        sources = await pipeline.run(
            project=project,
            max_results=5,
        )

        # Research completed successfully
        project.status = "sources_collected"

        db.commit()

        return {
            "project_id": project.id,
            "status": project.status,
            "source_count": len(sources),
            "sources": [
                {
                    "id": source.id,
                    "title": source.title,
                    "url": source.url,
                }
                for source in sources
            ],
        }

    except Exception as exc:
        # Something went wrong
        project.status = "failed"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# GET SOURCES FOR A RESEARCH PROJECT
# ---------------------------------------------------------

@router.get(
    "/{project_id}/sources",
    response_model=list[ResearchSourceResponse],
)
def get_research_sources(
    project_id: int,
    db: Session = Depends(get_db),
):
    # Check whether the project exists
    project = db.get(
        ResearchProject,
        project_id,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Research project not found",
        )

    # Get all sources belonging to this project
    sources = (
        db.query(ResearchSource)
        .filter(
            ResearchSource.project_id == project_id
        )
        .order_by(
            ResearchSource.created_at.desc()
        )
        .all()
    )

    return sources


@router.post("/{project_id}/search")
def search_research_knowledge(
    project_id: int,
    request: ResearchQuery,
):
    vector_store = ChromaStore()

    results = vector_store.search(
        query=request.query,
        n_results=request.n_results,
    )

    return results