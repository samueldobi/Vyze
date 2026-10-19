import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Numeric, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.enums import OpportunityStatus, OpportunityType


class Opportunity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "opportunities"
    __table_args__ = (
        Index(
            "uq_opportunities_with_job",
            "job_id",
            "opportunity_type",
            unique=True,
            postgresql_where=text("job_id IS NOT NULL"),
        ),
        Index(
            "uq_opportunities_without_job",
            "company_id",
            "opportunity_type",
            unique=True,
            postgresql_where=text("job_id IS NULL"),
        ),
        Index("ix_opportunities_type_status_score", "opportunity_type", "status", "score"),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="score_range"),
        CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="confidence_range",
        ),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("jobs.id"))
    opportunity_type: Mapped[OpportunityType] = mapped_column(
        Enum(
            OpportunityType,
            name="opportunity_type",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(
            OpportunityStatus,
            name="opportunity_status",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        default=OpportunityStatus.NEW,
        nullable=False,
    )
    score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    rationale: Mapped[str | None] = mapped_column(Text)
    owner_notes: Mapped[str | None] = mapped_column(Text)
    last_scored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
