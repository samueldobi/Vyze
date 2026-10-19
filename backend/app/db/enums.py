from enum import StrEnum


class RemoteScope(StrEnum):
    WORLDWIDE = "worldwide"
    COUNTRY_RESTRICTED = "country_restricted"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


class TriState(StrEnum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class JobState(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class OpportunityType(StrEnum):
    STARTUP_JOB = "startup_job"
    AGENCY_PARTNER = "agency_partner"
    DIRECT_CLIENT = "direct_client"


class OpportunityStatus(StrEnum):
    NEW = "new"
    RESEARCHING = "researching"
    QUALIFIED = "qualified"
    DRAFTED = "drafted"
    CONTACTED = "contacted"
    FOLLOW_UP_DUE = "follow_up_due"
    IN_CONVERSATION = "in_conversation"
    INTERVIEW_OR_PROPOSAL = "interview_or_proposal"
    WON = "won"
    LOST = "lost"
    ARCHIVED = "archived"


class OutreachStatus(StrEnum):
    DRAFT = "draft"
    APPROVED = "approved"
    SENT_MANUAL = "sent_manual"
    REPLIED = "replied"
    DECLINED = "declined"
    SUPPRESSED = "suppressed"


class VerificationState(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
