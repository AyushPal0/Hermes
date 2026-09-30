from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.services.agent.research_agent import ResearchAgent


class ResearchPipeline:

    def __init__(self, db: Session):

        self.db = db
        self.agent = ResearchAgent(db)

    async def run(
        self,
        project: ResearchProject,
    ):

        return await self.agent.run(
            project=project
        )