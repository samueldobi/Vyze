import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.enums import OutreachStatus


class Outreach(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "outreach"
    __table_args__ = (
        Index("ix_outreach_opportunity_status", "opportunity_id", "status"),
        Index("ix_outreach_next_follow_up_date", "next_follow_up_date"),
    )

    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("contacts.id"))
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255))
    draft: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OutreachStatus] = mapped_column(
        Enum(
            OutreachStatus,
            name="outreach_status",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        default=OutreachStatus.DRAFT,
        nullable=False,
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    replied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    next_follow_up_date: Mapped[date | None] = mapped_column(Date)


class SuppressionEntry(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "suppression_entries"

    normalized_destination: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
