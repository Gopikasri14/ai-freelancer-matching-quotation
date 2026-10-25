from fastapi import APIRouter
from .health import router as health_router
from .projects import router as project_router
from .freelancers import router as freelancer_router
from .matching import router as matching_router
from .quotations import router as quotation_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(project_router, prefix="/projects", tags=["projects"])
router.include_router(freelancer_router, prefix="/freelancers", tags=["freelancers"])
router.include_router(matching_router, prefix="/matching", tags=["matching"])
router.include_router(quotation_router, prefix="/quotations", tags=["quotations"])
