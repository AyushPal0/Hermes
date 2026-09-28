from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResearchSource(Base):

    __tablename__ = "research_sources"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("research_projects.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    snippet: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    content: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    author: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    published_at: Mapped[str] = mapped_column(
        String(100),
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )