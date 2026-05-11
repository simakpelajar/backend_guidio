import logging
from functools import lru_cache


def initialize_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


@lru_cache(maxsize=None)
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
