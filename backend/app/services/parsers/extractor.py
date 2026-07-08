import logging
from pathlib import Path
from typing import Dict

from app.services.parsers.image_parser import parse_image
from app.services.parsers.pdf_parser import parse_pdf
from app.services.parsers.text_parser import parse_text

logger = logging.getLogger(__name__)


async def extract_document_text(file_path: str) -> Dict[str, str]:
    """
    Detects file type based on extension and routes to the appropriate parser.
    Returns a dictionary with 'document_type' and 'text'.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()

    try:
        if ext == ".pdf":
            text = await parse_pdf(str(file_path))
            doc_type = "pdf"
        elif ext in {".png", ".jpg", ".jpeg"}:
            text = await parse_image(str(file_path))
            doc_type = "image"
        elif ext == ".txt":
            text = await parse_text(str(file_path))
            doc_type = "text"
        else:
            raise ValueError(f"Unsupported file extension for extraction: {ext}")

        return {"document_type": doc_type, "text": text}

    except Exception as e:
        logger.error(f"Extraction failed for {file_path}: {e}")
        raise
