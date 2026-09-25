from fastapi import APIRouter
from app.api.v1.health import router as health_router

api_router = APIRouter()

# Register sub-routers
api_router.include_router(health_router)

# Routers to be attached in subsequent milestones:
# api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(freelancers_router, prefix="/freelancers", tags=["Freelancers"])
# api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
# api_router.include_router(matching_router, prefix="/matching", tags=["Matching"])
# api_router.include_router(quotations_router, prefix="/quotations", tags=["Quotations"])
