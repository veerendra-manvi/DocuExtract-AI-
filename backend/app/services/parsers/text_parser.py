import asyncio
import logging

logger = logging.getLogger(__name__)


def _parse_text_sync(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except Exception as e:
        logger.error(f"Failed to read text file {file_path}: {e}")
        raise RuntimeError(f"Text parsing failed: {str(e)}") from e


async def parse_text(file_path: str) -> str:
    """
    Read text from a plain text file asynchronously using a thread pool.
    Handles UTF-8 encoding safely.
    """
    return await asyncio.to_thread(_parse_text_sync, file_path)
