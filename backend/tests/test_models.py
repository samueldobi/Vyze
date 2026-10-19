from app.db import model_registry  # noqa: F401
from app.db.base import Base


def test_phase_one_tables_are_registered() -> None:
    assert set(Base.metadata.tables) == {
        "activities",
        "companies",
        "company_signals",
        "company_sources",
        "contacts",
        "ingestion_runs",
        "jobs",
        "opportunities",
        "outreach",
        "score_components",
        "suppression_entries",
    }


def test_opportunity_deduplication_indexes_are_unique() -> None:
    table = Base.metadata.tables["opportunities"]
    indexes = {str(index.name): index for index in table.indexes}

    assert indexes["uq_opportunities_with_job"].unique is True
    assert indexes["uq_opportunities_without_job"].unique is True
