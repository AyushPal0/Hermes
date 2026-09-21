from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResearchProject(Base):
    __tablename__ = "research_projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    depth: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="deep",
    )

    sources: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="web",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="created",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )