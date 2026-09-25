import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is in the Python module search path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.api.v1.health import router as health_router

app = FastAPI(
    title="AI Freelancer Matching and Quotation Optimization System",
    description="Production-style API for AI-powered freelancer recommendations and quotation optimization.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 Routers
app.include_router(health_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def read_root():
    """
    Root entry point providing discovery links to docs and health status.
    """
    return {
        "message": "Welcome to AI Freelancer Matching and Quotation Optimization API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
