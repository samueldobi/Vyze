from collections.abc import AsyncIterator

import httpx
import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import Settings
from app.db.session import get_session
from app.main import create_app


class DatabaseTestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    test_database_url: str


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    engine = create_async_engine(DatabaseTestSettings().test_database_url)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        app = create_app(Settings(app_env="test"))

        async def override_session() -> AsyncIterator[AsyncSession]:
            yield session

        app.dependency_overrides[get_session] = override_session
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as api_client:
            yield api_client
        await session.close()
        await transaction.rollback()
    await engine.dispose()


@pytest.mark.asyncio
async def test_company_crud_filtering_and_pagination(client: httpx.AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/companies",
        json={
            "canonical_name": "  Acme   Labs  ",
            "normalized_domain": "https://www.Acme.example/about",
            "website_url": "https://acme.example",
            "headquarters_country": "us",
            "headquarters_region": "North America",
            "employee_size_min": 10,
            "employee_size_max": 50,
            "sector": "Software",
        },
    )
    assert create_response.status_code == 201
    company = create_response.json()
    assert company["canonical_name"] == "Acme Labs"
    assert company["normalized_domain"] == "acme.example"
    assert company["headquarters_country"] == "US"

    company_id = company["id"]
    list_response = await client.get(
        "/api/v1/companies",
        params={"search": "acme", "country": "us", "sort": "canonical_name"},
    )
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert list_response.json()["items"][0]["id"] == company_id

    update_response = await client.patch(
        f"/api/v1/companies/{company_id}", json={"employee_size_max": 75}
    )
    assert update_response.status_code == 200
    assert update_response.json()["employee_size_max"] == 75

    get_response = await client.get(f"/api/v1/companies/{company_id}")
    assert get_response.status_code == 200

    delete_response = await client.delete(f"/api/v1/companies/{company_id}")
    assert delete_response.status_code == 204
    assert (await client.get(f"/api/v1/companies/{company_id}")).status_code == 404


@pytest.mark.asyncio
async def test_duplicate_domain_returns_stable_conflict(client: httpx.AsyncClient) -> None:
    first = await client.post(
        "/api/v1/companies",
        json={"canonical_name": "First", "normalized_domain": "example.com"},
    )
    second = await client.post(
        "/api/v1/companies",
        json={"canonical_name": "Second", "normalized_domain": "www.example.com"},
    )

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "company_conflict"


@pytest.mark.asyncio
async def test_invalid_company_returns_stable_validation_error(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/v1/companies",
        json={"canonical_name": "Invalid", "normalized_domain": "localhost"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
