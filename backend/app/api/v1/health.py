from fastapi import APIRouter, Depends
from app.core.config import Settings, get_settings
from app.schemas.common import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
def get_health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """
    Health check endpoint to verify service status.
    """
    return HealthResponse(
        status="ok",
        service="ai-freelancer-system",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    )
