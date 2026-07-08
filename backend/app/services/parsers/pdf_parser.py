import asyncio
import logging

import fitz  # PyMuPDF
import pdfplumber

logger = logging.getLogger(__name__)


def _parse_pdf_sync(file_path: str) -> str:
    extracted_text = []

    try:
        with fitz.open(file_path) as doc:
            if doc.needs_pass:
                logger.warning(f"PDF {file_path} is password protected.")
                raise ValueError("PDF is password protected.")

            for page in doc:
                text = page.get_text()
                if text:
                    extracted_text.append(text)

        result = "\n".join(extracted_text).strip()
        if result:
            return result

        logger.warning(
            f"PyMuPDF extracted no text from {file_path}. Trying pdfplumber."
        )
    except Exception as e:
        logger.warning(
            f"PyMuPDF failed on {file_path} with error: {e}. Falling back to pdfplumber."
        )

    extracted_text.clear()
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
        return "\n".join(extracted_text).strip()
    except Exception as e2:
        logger.error(f"pdfplumber also failed on {file_path} with error: {e2}")
        raise RuntimeError(
            "Failed to extract text from PDF using both PyMuPDF and pdfplumber."
        ) from e2


async def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file asynchronously using a thread pool.
    Tries PyMuPDF first, falls back to pdfplumber on failure or empty extraction.
    """
    return await asyncio.to_thread(_parse_pdf_sync, file_path)
