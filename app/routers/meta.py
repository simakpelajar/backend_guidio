from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.vision import HealthResponse
from app.services.vision.model_loader import get_model_bundle

router = APIRouter(tags=["meta"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    settings = get_settings()
    bundle = get_model_bundle()
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        device=str(bundle.device),
        model_name=bundle.model_name,
    )


@router.get("/")
async def root():
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "describe_multipart": "POST /v1/vision/describe",
            "describe_base64": "POST /v1/vision/describe-base64",
        },
        "model": settings.preferred_model_name,
    }