import json
import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)


def _normalize_date(date_str: str) -> str:
    if not date_str:
        return None
    try:
        import dateutil.parser

        parsed = dateutil.parser.parse(str(date_str))
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        return date_str


def _normalize_number(val: Any) -> float:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    val_str = re.sub(r"[^\d\.\-]", "", str(val))
    try:
        return float(val_str)
    except ValueError:
        return None


def normalize_extracted_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes numeric fields, currency fields, and date fields extracted by the AI.
    """
    numeric_fields = {"subtotal", "tax", "discount", "total"}
    date_fields = {"invoice_date", "due_date"}

    for field in numeric_fields:
        if field in data and data[field] is not None:
            val = _normalize_number(data[field])
            if field == "discount" and val is not None:
                val = abs(val)
            data[field] = val

    for field in date_fields:
        if field in data and data[field] is not None:
            data[field] = _normalize_date(data[field])

    if data.get("line_items") and isinstance(data["line_items"], list):
        for item in data["line_items"]:
            for n_field in ["quantity", "unit_price", "amount"]:
                if n_field in item and item[n_field] is not None:
                    item[n_field] = _normalize_number(item[n_field])

    # Normalize currency
    if data.get("currency") and isinstance(data["currency"], str):
        c_str = data["currency"].strip().upper()
        # Keep only letters or basic symbols
        c_str = re.sub(r"[^A-Z$€£¥₹]", "", c_str)
        if len(c_str) > 3 and not c_str.isalpha():
            c_str = c_str[:1]  # Take first symbol
        data["currency"] = c_str if c_str else None

    return data


def parse_ai_response(raw_response: str) -> Dict[str, Any]:
    """
    Validates and parses the AI output into a JSON dictionary.
    Uses regex to forcefully extract the outermost JSON block, bypassing conversational wrappers.
    """
    # Regex to capture the first JSON object block, robust against markdown/chatter
    match = re.search(r"\{.*\}", raw_response, re.DOTALL)

    if match:
        cleaned = match.group(0)
    else:
        cleaned = raw_response.strip()

    try:
        data = json.loads(cleaned)
        return normalize_extracted_data(data)
    except json.JSONDecodeError as e:
        logger.error(
            f"Failed to parse AI JSON response. Raw string: {raw_response[:150]}..."
        )
        raise ValueError("Invalid JSON format returned by AI.") from e
