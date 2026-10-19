import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.enums import JobState, RemoteScope, TriState


class Job(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("source_name", "source_external_id", name="uq_jobs_source_identity"),
        Index("ix_jobs_company_state", "company_id", "state"),
        Index("ix_jobs_remote_scope", "remote_scope"),
        Index("ix_jobs_last_seen_at", "last_seen_at"),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    location_text: Mapped[str | None] = mapped_column(String(255))
    employment_type: Mapped[str | None] = mapped_column(String(80))
    remote_scope: Mapped[RemoteScope] = mapped_column(
        Enum(
            RemoteScope, name="remote_scope", values_callable=lambda enum: [e.value for e in enum]
        ),
        default=RemoteScope.UNKNOWN,
        nullable=False,
    )
    eligible_countries: Mapped[list[str] | None] = mapped_column(JSONB)
    sponsorship: Mapped[TriState] = mapped_column(
        Enum(
            TriState, name="sponsorship_state", values_callable=lambda enum: [e.value for e in enum]
        ),
        default=TriState.UNKNOWN,
        nullable=False,
    )
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    state: Mapped[JobState] = mapped_column(
        Enum(JobState, name="job_state", values_callable=lambda enum: [e.value for e in enum]),
        default=JobState.UNKNOWN,
        nullable=False,
    )
    source_evidence: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
