from dataclasses import dataclass
from typing import Optional

import torch
from transformers import BlipForConditionalGeneration, BlipProcessor

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class BlipModelBundle:
    processor: BlipProcessor
    model: BlipForConditionalGeneration
    device: torch.device
    model_name: str


_bundle: Optional[BlipModelBundle] = None


def _load_bundle(model_name: str) -> BlipModelBundle:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Loading BLIP model %s on %s", model_name, device)

    processor = BlipProcessor.from_pretrained(model_name, use_fast=False)
    model = BlipForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
    ).to(device)
    model.eval()

    return BlipModelBundle(
        processor=processor,
        model=model,
        device=device,
        model_name=model_name,
    )


def load_model(force_reload: bool = False) -> BlipModelBundle:
    global _bundle

    if _bundle is not None and not force_reload:
        return _bundle

    settings = get_settings()

    try:
        _bundle = _load_bundle(settings.preferred_model_name)
    except Exception as preferred_error:
        logger.warning(
            "Preferred BLIP model failed, falling back to base model: %s",
            preferred_error,
        )
        _bundle = _load_bundle(settings.fallback_model_name)

    return _bundle


def get_model_bundle() -> BlipModelBundle:
    return load_model()


def is_model_loaded() -> bool:
    return _bundle is not None
