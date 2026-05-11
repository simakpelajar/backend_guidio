def clean_caption(caption: str) -> str:
    normalized = " ".join(caption.strip().split())

    if normalized and normalized[0].islower():
        normalized = normalized[0].upper() + normalized[1:]

    return normalized
