import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.companies.models import Company
from app.modules.companies.schemas import CompanySortField, SortDirection


class CompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, values: dict[str, object]) -> Company:
        company = Company(**values)
        self.session.add(company)
        await self.session.flush()
        await self.session.refresh(company)
        return company

    async def get(self, company_id: uuid.UUID) -> Company | None:
        return await self.session.get(Company, company_id)

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
    ) -> tuple[list[Company], int]:
        query = select(Company)
        if search:
            query = query.where(Company.canonical_name.ilike(f"%{search}%"))
        if country:
            query = query.where(Company.headquarters_country == country.upper())
        if region:
            query = query.where(Company.headquarters_region == region)
        if sector:
            query = query.where(Company.sector == sector)
        total = await self.session.scalar(select(func.count()).select_from(query.subquery()))
        sort_column = getattr(Company, sort)
        ordering = sort_column.asc() if direction == "asc" else sort_column.desc()
        query = (
            query.order_by(ordering, Company.id.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.scalars(query)
        return list(result), total or 0

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
