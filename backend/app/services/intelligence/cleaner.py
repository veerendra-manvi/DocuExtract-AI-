import logging
import re

logger = logging.getLogger(__name__)

# Pre-compile regex for performance
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
MULTI_NEWLINE_RE = re.compile(r"\n{3,}")
STRAY_PUNCT_RE = re.compile(r"^[^\w\s]{1,2}$")
STRAY_CHARS = {"|", "_", "~", "`", "\\", "/", "^", ".", "-", ":", ","}


def clean_text(raw_text: str) -> str:
    """
    Cleans extracted raw text by normalizing whitespaces, tabs,
    duplicate lines, and safe OCR artifacts.
    """
    if not raw_text:
        return ""

    try:
        # Normalize tabs to spaces
        text = raw_text.replace("\t", " ")

        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                cleaned_lines.append("")
                continue

            # Remove excessive whitespace within lines
            stripped = MULTI_SPACE_RE.sub(" ", stripped)

            # Remove isolated random punctuation which is likely OCR noise
            if STRAY_PUNCT_RE.match(stripped) and stripped in STRAY_CHARS:
                continue

            cleaned_lines.append(stripped)

        # Remove duplicate blank lines (reduce multiple newlines to max 2)
        cleaned_text = "\n".join(cleaned_lines)
        cleaned_text = MULTI_NEWLINE_RE.sub("\n\n", cleaned_text)

        return cleaned_text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
        return raw_text.strip()
