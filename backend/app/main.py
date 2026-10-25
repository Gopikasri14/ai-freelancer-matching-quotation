from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .db import Base, engine
from .api.v1.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

# CORS configuration
allowed_origins = [
    x.strip()
    for x in settings.cors_origins.split(",")
    if x.strip()
]

# Allow the deployed Vercel frontend
vercel_frontend = "https://ai-freelancer-matching-quotation-jade.vercel.app"

if vercel_frontend not in allowed_origins:
    allowed_origins.append(vercel_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "AI Freelancer Matching and Quotation Optimization API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }