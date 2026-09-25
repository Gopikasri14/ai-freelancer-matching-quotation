from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """
    Health check endpoint to verify service status.
    """
    return HealthResponse(
        status="ok",
        service="ai-freelancer-system"
    )
