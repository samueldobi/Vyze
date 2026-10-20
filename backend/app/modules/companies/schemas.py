import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    TypeAdapter,
    field_validator,
    model_validator,
)

from app.modules.companies.normalization import normalize_domain

_http_url_adapter = TypeAdapter(HttpUrl)


def _clean_name_value(value: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError("Company name cannot be blank.")
    return cleaned


def _clean_domain_value(value: str | None) -> str | None:
    return normalize_domain(value) if value else None


def _validate_website_value(value: str | None) -> str | None:
    return str(_http_url_adapter.validate_python(value)) if value else None


def _uppercase_code_value(value: str | None) -> str | None:
    return value.upper() if value else None


class CompanyFields(BaseModel):
    canonical_name: str = Field(min_length=1, max_length=255)
    normalized_domain: str | None = Field(default=None, max_length=253)
    website_url: str | None = None
    headquarters_country: str | None = Field(default=None, min_length=2, max_length=2)
    headquarters_region: str | None = Field(default=None, max_length=100)
    employee_size_min: int | None = Field(default=None, ge=0)
    employee_size_max: int | None = Field(default=None, ge=0)
    sector: str | None = Field(default=None, max_length=120)
    funding_stage: str | None = Field(default=None, max_length=80)
    funding_amount: Decimal | None = Field(default=None, ge=0, max_digits=18, decimal_places=2)
    funding_currency: str | None = Field(default=None, min_length=3, max_length=3)
    funding_date: date | None = None

    @field_validator("canonical_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return _clean_name_value(value)

    @field_validator("normalized_domain")
    @classmethod
    def clean_domain(cls, value: str | None) -> str | None:
        return _clean_domain_value(value)

    @field_validator("website_url")
    @classmethod
    def validate_website(cls, value: str | None) -> str | None:
        return _validate_website_value(value)

    @field_validator("headquarters_country", "funding_currency")
    @classmethod
    def uppercase_codes(cls, value: str | None) -> str | None:
        return _uppercase_code_value(value)

    @model_validator(mode="after")
    def validate_employee_range(self) -> Self:
        if (
            self.employee_size_min is not None
            and self.employee_size_max is not None
            and self.employee_size_max < self.employee_size_min
        ):
            raise ValueError("employee_size_max must be greater than or equal to employee_size_min")
        return self


class CompanyCreate(CompanyFields):
    pass


class CompanyUpdate(BaseModel):
    canonical_name: str | None = Field(default=None, min_length=1, max_length=255)
    normalized_domain: str | None = Field(default=None, max_length=253)
    website_url: str | None = None
    headquarters_country: str | None = Field(default=None, min_length=2, max_length=2)
    headquarters_region: str | None = Field(default=None, max_length=100)
    employee_size_min: int | None = Field(default=None, ge=0)
    employee_size_max: int | None = Field(default=None, ge=0)
    sector: str | None = Field(default=None, max_length=120)
    funding_stage: str | None = Field(default=None, max_length=80)
    funding_amount: Decimal | None = Field(default=None, ge=0, max_digits=18, decimal_places=2)
    funding_currency: str | None = Field(default=None, min_length=3, max_length=3)
    funding_date: date | None = None

    @field_validator("canonical_name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        return _clean_name_value(value) if value is not None else None

    @field_validator("normalized_domain")
    @classmethod
    def clean_domain(cls, value: str | None) -> str | None:
        return _clean_domain_value(value)

    @field_validator("website_url")
    @classmethod
    def validate_website(cls, value: str | None) -> str | None:
        return _validate_website_value(value)

    @field_validator("headquarters_country", "funding_currency")
    @classmethod
    def uppercase_codes(cls, value: str | None) -> str | None:
        return _uppercase_code_value(value)


class CompanyRead(CompanyFields):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CompanyList(BaseModel):
    items: list[CompanyRead]
    page: int
    page_size: int
    total: int
    pages: int


CompanySortField = Literal["canonical_name", "created_at", "updated_at", "employee_size_min"]
SortDirection = Literal["asc", "desc"]
