import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDPrimaryKeyMixin


class ScoreComponent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "score_components"
    __table_args__ = (
        UniqueConstraint(
            "opportunity_id", "criterion", "model_version", name="uq_score_components_version"
        ),
        Index("ix_score_components_opportunity_id", "opportunity_id"),
        CheckConstraint("weight >= 0 AND weight <= 100", name="weight_range"),
        CheckConstraint(
            "normalized_value IS NULL OR (normalized_value >= 0 AND normalized_value <= 1)",
            name="normalized_value_range",
        ),
        CheckConstraint(
            "contribution IS NULL OR (contribution >= 0 AND contribution <= 100)",
            name="contribution_range",
        ),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="confidence_range"),
    )

    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False
    )
    criterion: Mapped[str] = mapped_column(String(120), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    normalized_value: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))
    contribution: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    evidence: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
