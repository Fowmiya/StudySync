from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PerformanceRecord(Base):
    __tablename__ = "performance_records"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False,
        index=True
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    max_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    exam_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="performance_records"
    )