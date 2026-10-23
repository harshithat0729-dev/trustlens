"""TrustLens API - app factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import link, message, media, claim

app = FastAPI(
    title="TrustLens API",
    version="0.1.0",
    description="Multimodal, multilingual digital trust & safety assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(link.router)
app.include_router(message.router)
app.include_router(media.router)
app.include_router(claim.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "trustlens", "version": app.version}


@app.get("/", tags=["meta"])
def root():
    return {"name": "TrustLens", "tagline": "Before you trust it, check it.",
            "docs": "/docs"}
