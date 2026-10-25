from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .db import Base, engine
from .api.v1.router import router
from .seed import main as seed_demo_freelancers


# Create database tables
Base.metadata.create_all(bind=engine)

# Add sample freelancers if the database is empty
seed_demo_freelancers()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)


# Configure CORS
allowed_origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

# Allow deployed Vercel frontend
vercel_frontend = (
    "https://ai-freelancer-matching-quotation-jade.vercel.app"
)

if vercel_frontend not in allowed_origins:
    allowed_origins.append(vercel_frontend)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(
    router,
    prefix="/api/v1"
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AI Freelancer Matching and Quotation Optimization API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }