from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.core.logger import get_logger
from app.schemas.vision import DescribeSceneRequest, DescribeSceneResponse
from app.services.vision.caption_service import (
    describe_scene_from_base64,
    describe_scene_from_bytes,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/v1/vision", tags=["vision"])


@router.post("/describe", response_model=DescribeSceneResponse)
async def describe_scene(file: UploadFile = File(...)):
    settings = get_settings()

    if file.content_type not in settings.allowed_image_content_types:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported image type: {file.content_type}. "
                "Use JPEG, PNG, or WebP."
            ),
        )

    content = await file.read()
    return describe_scene_from_bytes(content)


@router.post("/describe-base64", response_model=DescribeSceneResponse)
async def describe_scene_base64(request: DescribeSceneRequest):
    return describe_scene_from_base64(request.image_base64)
