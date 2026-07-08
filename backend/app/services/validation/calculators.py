import re
from typing import Any, Dict, List


def parse_float(val: Any) -> float:
    """Safely parse a float from a string, handling commas, spaces, and currency symbols."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)

    # Strip spaces, commas, and currency characters, retaining only digits, dots, and minus
    val_str = re.sub(r"[^\d\.\-]", "", str(val))
    try:
        return float(val_str)
    except ValueError:
        return 0.0


def sum_line_items(line_items: List[Dict[str, Any]]) -> float:
    """Calculates the sum of all line item amounts safely."""
    if not line_items:
        return 0.0
    return sum(parse_float(item.get("amount")) for item in line_items)


def calculate_expected_total(subtotal: float, tax: float, discount: float) -> float:
    """Calculates grand total based on components."""
    return subtotal + tax - discount


def calculate_completeness(data: Dict[str, Any], required_fields: List[str]) -> float:
    """Returns completeness percentage."""
    if not required_fields:
        return 100.0
    filled = sum(
        1
        for field in required_fields
        if data.get(field) is not None and data.get(field) != ""
    )
    return round((filled / len(required_fields)) * 100, 2)
