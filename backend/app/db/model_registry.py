"""Import all persistence models so Alembic can discover their tables."""

from app.modules.activities.models import Activity
from app.modules.companies.models import Company, CompanySource
from app.modules.contacts.models import Contact
from app.modules.ingestion.models import IngestionRun
from app.modules.jobs.models import Job
from app.modules.opportunities.models import Opportunity
from app.modules.outreach.models import Outreach, SuppressionEntry
from app.modules.scoring.models import ScoreComponent
from app.modules.signals.models import CompanySignal

__all__ = [
    "Activity",
    "Company",
    "CompanySignal",
    "CompanySource",
    "Contact",
    "IngestionRun",
    "Job",
    "Opportunity",
    "Outreach",
    "ScoreComponent",
    "SuppressionEntry",
]
