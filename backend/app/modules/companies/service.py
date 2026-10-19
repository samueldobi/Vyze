import uuid
from math import ceil

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApplicationError
from app.modules.companies.models import Company
from app.modules.companies.repository import CompanyRepository
from app.modules.companies.schemas import (
    CompanyCreate,
    CompanyList,
    CompanyRead,
    CompanySortField,
    CompanyUpdate,
    SortDirection,
)


class CompanyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = CompanyRepository(session)

    async def create(self, payload: CompanyCreate) -> Company:
        try:
            company = await self.repository.create(payload.model_dump())
            await self.session.commit()
            return company
        except IntegrityError as exception:
            await self.session.rollback()
            raise ApplicationError(
                status_code=409,
                code="company_conflict",
                message="A company with this normalized domain already exists.",
            ) from exception

    async def get(self, company_id: uuid.UUID) -> Company:
        company = await self.repository.get(company_id)
        if company is None:
            raise ApplicationError(
                status_code=404,
                code="company_not_found",
                message="Company not found.",
            )
        return company

    async def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None,
        country: str | None,
        region: str | None,
        sector: str | None,
        sort: CompanySortField,
        direction: SortDirection,
    ) -> CompanyList:
        companies, total = await self.repository.list(
            page=page,
            page_size=page_size,
            search=search,
            country=country,
            region=region,
            sector=sector,
            sort=sort,
            direction=direction,
        )
        return CompanyList(
            items=[CompanyRead.model_validate(company) for company in companies],
            page=page,
            page_size=page_size,
            total=total,
            pages=ceil(total / page_size) if total else 0,
        )

    async def update(self, company_id: uuid.UUID, payload: CompanyUpdate) -> Company:
        company = await self.get(company_id)
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return company
        if updates.get("canonical_name") is None and "canonical_name" in updates:
            raise ApplicationError(
                status_code=422,
                code="validation_error",
                message="canonical_name cannot be null.",
            )
        minimum = updates.get("employee_size_min", company.employee_size_min)
        maximum = updates.get("employee_size_max", company.employee_size_max)
        if minimum is not None and maximum is not None and maximum < minimum:
            raise ApplicationError(
                status_code=422,
                code="validation_error",
                message="employee_size_max must be greater than or equal to employee_size_min.",
            )
        for field, value in updates.items():
            setattr(company, field, value)
        try:
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(company)
            return company
        except IntegrityError as exception:
            await self.session.rollback()
            raise ApplicationError(
                status_code=409,
                code="company_conflict",
                message="A company with this normalized domain already exists.",
            ) from exception

    async def delete(self, company_id: uuid.UUID) -> None:
        company = await self.get(company_id)
        try:
            await self.repository.delete(company)
            await self.session.commit()
        except IntegrityError as exception:
            await self.session.rollback()
            raise ApplicationError(
                status_code=409,
                code="company_in_use",
                message="A company with dependent records cannot be deleted.",
            ) from exception
