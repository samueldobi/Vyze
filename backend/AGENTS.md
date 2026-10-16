# Backend Instructions

The project-wide instructions in `../AGENTS.md` apply here.

- Use Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, and HTTPX.
- Prefer async endpoints and keep database session usage consistently async.
- Use local PostgreSQL through `DATABASE_URL`; do not introduce a hosted database or managed authentication dependency.
- Keep the backend a modular monolith with business rules independent of FastAPI, SQLAlchemy, and external integrations.
- Separate persistence models, transport schemas, repositories, services, and routers when each layer has real behavior; do not create empty layers for symmetry.
- Use dependency injection for database sessions and external clients. Keep network requests outside database transactions.
- Expose versioned routes under `/api/v1` and return stable error shapes. Never expose ORM models directly as API responses.
- Use UTC-aware timestamps, typed module boundaries, parameterized database access, and Alembic migrations for schema changes.
- Preserve source URLs, observation timestamps, provenance, confidence, and explicit unknown values.
- Add or update tests alongside each implementation slice. Never use live third-party APIs in automated tests.
- Do not install dependencies without the user's explicit approval; report the required install command and wait for the user to run it.

