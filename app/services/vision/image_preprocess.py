from PIL import Image

from app.core.config import get_settings


def resize_image(image: Image.Image) -> Image.Image:
    settings = get_settings()
    prepared_image = image.convert("RGB")

    if (
        prepared_image.width > settings.max_image_size
        or prepared_image.height > settings.max_image_size
    ):
        prepared_image.thumbnail(
            (settings.max_image_size, settings.max_image_size),
            Image.Resampling.LANCZOS,
        )

    return prepared_image
