"""Process-wide logging bootstrap (call once from `main` before serving traffic)."""

import logging
import sys


def configure_logging(level_name: str) -> None:
    """Attach a stdout `basicConfig` formatter suitable for structured grepping.

    Args:
        level_name: Log level name (e.g. ``INFO``) as stored in settings.
    """
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(asctime)s %(name)s %(message)s",
        stream=sys.stdout,
    )
