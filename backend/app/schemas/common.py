from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

DataT = TypeVar("DataT")


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = "ok"
    service: str = "ai-freelancer-system"
    version: Optional[str] = None
    environment: Optional[str] = None


class StandardResponse(BaseModel, Generic[DataT]):
    """Standardized API response envelope for consistent client consumption."""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[DataT] = None
