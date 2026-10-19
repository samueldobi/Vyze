# Vyze

Vyze is a local-first opportunity discovery and relationship-management application.

## Prerequisites

- Python 3.12+
- PostgreSQL 18 (PostgreSQL 15+ is supported)
- Node.js tooling will be documented when the frontend is initialized

## PostgreSQL

Start the Homebrew PostgreSQL 18 server on demand:

```bash
/opt/homebrew/opt/postgresql@18/bin/pg_ctl \
  -D /opt/homebrew/var/postgresql@18 \
  start
```

The local setup uses an existing PostgreSQL role named `admin` and two databases:

- `vyze_db` for local development
- `vyze_test_db` for isolated integration and migration tests

Create them from an administrator connection if they do not exist:

```sql
CREATE DATABASE vyze_db OWNER admin;
CREATE DATABASE vyze_test_db OWNER admin;
```

Copy the environment template and supply local credentials. Never commit `.env`.

```bash
cp .env.example .env
```

Stop PostgreSQL when finished:

```bash
/opt/homebrew/opt/postgresql@18/bin/pg_ctl \
  -D /opt/homebrew/var/postgresql@18 \
  stop
```

## Backend setup

The user installs dependencies explicitly; automation must not install them without permission.

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Apply database migrations:

```bash
alembic upgrade head
```

Start the API on the loopback interface:

```bash
uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

The health endpoint is `http://127.0.0.1:8000/api/v1/health`; OpenAPI documentation is
available at `http://127.0.0.1:8000/docs`.

Stop the development server with `Ctrl+C`.

### Company API

The first Phase 1 vertical slice is available under `/api/v1/companies`:

- `POST /api/v1/companies`
- `GET /api/v1/companies`
- `GET /api/v1/companies/{company_id}`
- `PATCH /api/v1/companies/{company_id}`
- `DELETE /api/v1/companies/{company_id}`

The list endpoint supports `page`, `page_size`, `search`, `country`, `region`, `sector`,
`sort`, and `direction`. The generated OpenAPI page documents the allowed sort fields and
request/response schemas.

## Backend quality checks

Run from `backend/` with the virtual environment active:

```bash
ruff check .
ruff format --check .
mypy app
pytest
alembic check
```

`alembic check` connects to `vyze_db` and confirms that model metadata matches the current
migration head.
