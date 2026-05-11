from base64 import b64decode
from io import BytesIO

from PIL import Image


def load_rgb_image_from_bytes(content: bytes) -> Image.Image:
    return Image.open(BytesIO(content)).convert("RGB")


def load_rgb_image_from_base64(image_base64: str) -> Image.Image:
    return load_rgb_image_from_bytes(b64decode(image_base64))
