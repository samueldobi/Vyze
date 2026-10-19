import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.companies.schemas import (
    CompanyCreate,
    CompanyList,
    CompanyRead,
    CompanySortField,
    CompanyUpdate,
    SortDirection,
)
from app.modules.companies.service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])
SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(payload: CompanyCreate, session: SessionDependency) -> CompanyRead:
    company = await CompanyService(session).create(payload)
    return CompanyRead.model_validate(company)


@router.get("", response_model=CompanyList)
async def list_companies(
    session: SessionDependency,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
    search: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    country: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    region: Annotated[str | None, Query(max_length=100)] = None,
    sector: Annotated[str | None, Query(max_length=120)] = None,
    sort: CompanySortField = "created_at",
    direction: SortDirection = "desc",
) -> CompanyList:
    return await CompanyService(session).list(
        page=page,
        page_size=page_size,
        search=search,
        country=country,
        region=region,
        sector=sector,
        sort=sort,
        direction=direction,
    )


@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(company_id: uuid.UUID, session: SessionDependency) -> CompanyRead:
    company = await CompanyService(session).get(company_id)
    return CompanyRead.model_validate(company)


@router.patch("/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: uuid.UUID, payload: CompanyUpdate, session: SessionDependency
) -> CompanyRead:
    company = await CompanyService(session).update(company_id, payload)
    return CompanyRead.model_validate(company)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: uuid.UUID, session: SessionDependency) -> Response:
    await CompanyService(session).delete(company_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
