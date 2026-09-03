from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="subjects"
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    performance_records: Mapped[list["PerformanceRecord"]] = relationship(
        "PerformanceRecord",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    study_sessions: Mapped[list["StudySession"]] = relationship(
        "StudySession",
        back_populates="subject",
        cascade="all, delete-orphan"
    )