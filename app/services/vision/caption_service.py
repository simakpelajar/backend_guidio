import time

import torch

from app.core.config import get_settings
from app.core.logger import get_logger
from app.schemas.vision import DescribeSceneResponse
from app.services.vision.image_preprocess import resize_image
from app.services.vision.model_loader import get_model_bundle
from app.services.vision.postprocess import clean_caption
from app.utils.file_utils import load_rgb_image_from_base64, load_rgb_image_from_bytes

logger = get_logger(__name__)


def describe_caption(image) -> str:
    settings = get_settings()
    bundle = get_model_bundle()
    prepared_image = resize_image(image)

    inputs = bundle.processor(prepared_image, return_tensors="pt").to(bundle.device)

    with torch.no_grad():
        output = bundle.model.generate(
            **inputs,
            max_length=settings.max_caption_length,
            num_beams=settings.num_beams,
            temperature=settings.temperature,
        )

    caption = bundle.processor.decode(output[0], skip_special_tokens=True)
    return clean_caption(caption)


def describe_scene_from_bytes(content: bytes) -> DescribeSceneResponse:
    start_time = time.time()
    image = load_rgb_image_from_bytes(content)
    description = describe_caption(image)
    processing_time_ms = (time.time() - start_time) * 1000

    logger.info("Generated description in %.2fms: %s", processing_time_ms, description)

    return DescribeSceneResponse(
        description=description,
        confidence=get_settings().default_confidence,
        processing_time_ms=processing_time_ms,
    )


def describe_scene_from_base64(image_base64: str) -> DescribeSceneResponse:
    start_time = time.time()
    image = load_rgb_image_from_base64(image_base64)
    description = describe_caption(image)
    processing_time_ms = (time.time() - start_time) * 1000

    logger.info("Generated description in %.2fms: %s", processing_time_ms, description)

    return DescribeSceneResponse(
        description=description,
        confidence=get_settings().default_confidence,
        processing_time_ms=processing_time_ms,
    )
