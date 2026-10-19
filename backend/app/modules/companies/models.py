import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Company(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("ix_companies_headquarters_region", "headquarters_region"),
        Index("ix_companies_sector", "sector"),
        CheckConstraint(
            "employee_size_min IS NULL OR employee_size_min >= 0",
            name="employee_size_min_nonnegative",
        ),
        CheckConstraint(
            "employee_size_max IS NULL OR employee_size_max >= employee_size_min",
            name="employee_size_range_valid",
        ),
        CheckConstraint(
            "funding_amount IS NULL OR funding_amount >= 0", name="funding_amount_nonnegative"
        ),
    )

    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_domain: Mapped[str | None] = mapped_column(String(253), unique=True)
    website_url: Mapped[str | None] = mapped_column(Text)
    headquarters_country: Mapped[str | None] = mapped_column(String(2))
    headquarters_region: Mapped[str | None] = mapped_column(String(100))
    employee_size_min: Mapped[int | None]
    employee_size_max: Mapped[int | None]
    sector: Mapped[str | None] = mapped_column(String(120))
    funding_stage: Mapped[str | None] = mapped_column(String(80))
    funding_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    funding_currency: Mapped[str | None] = mapped_column(String(3))
    funding_date: Mapped[date | None] = mapped_column(Date)


class CompanySource(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "company_sources"
    __table_args__ = (
        UniqueConstraint("source_name", "external_id", name="uq_company_sources_identity"),
        Index("ix_company_sources_company_id", "company_id"),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    raw_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
