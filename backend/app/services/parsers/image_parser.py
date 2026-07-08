import asyncio
import logging

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger(__name__)

# Configure Tesseract path since it is not in the system PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _parse_image_sync(file_path: str) -> str:
    try:
        with Image.open(file_path) as img:
            # 1. Convert to grayscale
            img = img.convert("L")

            # 2. Improve contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)

            # 3. Reduce noise
            img = img.filter(ImageFilter.MedianFilter())

            # Extract text with optimized layout analysis config for OCR quality
            custom_config = r"--oem 3 --psm 3"
            text = pytesseract.image_to_string(img, config=custom_config)
            return text.strip()

    except Exception as e:
        logger.error(f"Failed to extract text from image {file_path}: {e}")
        raise RuntimeError(f"Image parsing failed: {str(e)}") from e


async def parse_image(file_path: str) -> str:
    """
    Extract text from an image asynchronously using a thread pool.
    Preprocesses the image for better OCR results.
    """
    return await asyncio.to_thread(_parse_image_sync, file_path)
