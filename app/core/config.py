import os
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Guidio Vision API"
    api_prefix: str = "/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    preferred_model_name: str = "Salesforce/blip-image-captioning-large"
    fallback_model_name: str = "Salesforce/blip-image-captioning-base"
    max_image_size: int = 1024
    max_caption_length: int = 100
    num_beams: int = 5
    temperature: float = 0.7
    default_confidence: float = 0.95
    allowed_image_content_types: list[str] = Field(
        default_factory=lambda: ["image/jpeg", "image/png", "image/webp"]
    )

    @classmethod
    def from_env(cls) -> "Settings":
        cors_origins = os.getenv("CORS_ORIGINS", "*")

        return cls(
            app_name=os.getenv("APP_NAME", "Guidio Vision API"),
            api_prefix=os.getenv("API_PREFIX", "/v1"),
            cors_origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],
            preferred_model_name=os.getenv(
                "PREFERRED_MODEL_NAME", "Salesforce/blip-image-captioning-large"
            ),
            fallback_model_name=os.getenv(
                "FALLBACK_MODEL_NAME", "Salesforce/blip-image-captioning-base"
            ),
            max_image_size=int(os.getenv("MAX_IMAGE_SIZE", "1024")),
            max_caption_length=int(os.getenv("MAX_CAPTION_LENGTH", "100")),
            num_beams=int(os.getenv("NUM_BEAMS", "5")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            default_confidence=float(os.getenv("DEFAULT_CONFIDENCE", "0.95")),
            allowed_image_content_types=[
                content_type.strip()
                for content_type in os.getenv(
                    "ALLOWED_IMAGE_CONTENT_TYPES",
                    "image/jpeg,image/png,image/webp",
                ).split(",")
                if content_type.strip()
            ],
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()
