from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.companies.router import router as companies_router


class HealthResponse(BaseModel):
    status: str
    service: str


router = APIRouter(prefix="/api/v1")
router.include_router(companies_router)


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="vyze")
