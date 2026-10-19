import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.enums import VerificationState


class Contact(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "contacts"
    __table_args__ = (Index("ix_contacts_company_role", "company_id", "role_category"),)

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    public_name: Mapped[str] = mapped_column(String(255), nullable=False)
    public_title: Mapped[str | None] = mapped_column(String(255))
    role_category: Mapped[str] = mapped_column(String(100), nullable=False)
    public_business_email: Mapped[str | None] = mapped_column(String(320))
    contact_url: Mapped[str | None] = mapped_column(Text)
    provenance_url: Mapped[str] = mapped_column(Text, nullable=False)
    verification_state: Mapped[VerificationState] = mapped_column(
        Enum(
            VerificationState,
            name="verification_state",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        default=VerificationState.UNKNOWN,
        nullable=False,
    )
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
