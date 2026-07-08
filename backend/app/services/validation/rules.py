import math
from typing import Any, Dict, List

import dateutil.parser

from app.services.validation.calculators import (calculate_expected_total,
                                                 parse_float, sum_line_items)
from app.services.validation.report import ValidationCheck

ALLOWED_CURRENCIES = {"INR", "USD", "EUR", "GBP", "AED", "JPY", "AUD", "CAD"}
TOLERANCE = 0.01


def validate_dates(data: Dict[str, Any]) -> List[ValidationCheck]:
    checks = []
    inv_date_str = data.get("invoice_date")
    due_date_str = data.get("due_date")

    inv_date = None
    due_date = None

    if inv_date_str:
        try:
            # Force timezone-naive for safe comparison
            inv_date = dateutil.parser.parse(str(inv_date_str)).replace(tzinfo=None)
            checks.append(
                ValidationCheck(
                    rule="Invoice Date Format",
                    status="PASS",
                    actual=inv_date_str,
                    message="Invoice date is valid.",
                )
            )
        except Exception:
            checks.append(
                ValidationCheck(
                    rule="Invoice Date Format",
                    status="FAIL",
                    actual=inv_date_str,
                    message="Invoice date is invalid.",
                )
            )

    if due_date_str:
        try:
            due_date = dateutil.parser.parse(str(due_date_str)).replace(tzinfo=None)
            checks.append(
                ValidationCheck(
                    rule="Due Date Format",
                    status="PASS",
                    actual=due_date_str,
                    message="Due date is valid.",
                )
            )
        except Exception:
            checks.append(
                ValidationCheck(
                    rule="Due Date Format",
                    status="FAIL",
                    actual=due_date_str,
                    message="Due date is invalid.",
                )
            )

    if inv_date and due_date:
        if due_date >= inv_date:
            checks.append(
                ValidationCheck(
                    rule="Date Logic",
                    status="PASS",
                    expected=">= Invoice Date",
                    actual=due_date_str,
                    message="Due date is logically after or equal to invoice date.",
                )
            )
        else:
            checks.append(
                ValidationCheck(
                    rule="Date Logic",
                    status="FAIL",
                    expected=">= Invoice Date",
                    actual=due_date_str,
                    message="Due date cannot be before invoice date.",
                )
            )

    return checks


def validate_currency(data: Dict[str, Any]) -> ValidationCheck:
    currency = data.get("currency")
    if not currency:
        return ValidationCheck(
            rule="Currency Validation", status="WARNING", message="Currency is missing."
        )

    currency_upper = str(currency).upper().strip()
    if currency_upper in ALLOWED_CURRENCIES:
        return ValidationCheck(
            rule="Currency Validation",
            status="PASS",
            actual=currency_upper,
            message=f"Currency {currency_upper} is supported.",
        )

    return ValidationCheck(
        rule="Currency Validation",
        status="WARNING",
        actual=currency,
        message=f"Currency {currency} is unknown/unsupported.",
    )


def validate_invoice_fields(data: Dict[str, Any]) -> List[ValidationCheck]:
    checks = []
    inv_num = data.get("invoice_number")
    if inv_num:
        checks.append(
            ValidationCheck(
                rule="Invoice Number Exists",
                status="PASS",
                actual=inv_num,
                message="Invoice number is present.",
            )
        )
    else:
        checks.append(
            ValidationCheck(
                rule="Invoice Number Exists",
                status="FAIL",
                message="Invoice number is missing.",
            )
        )

    vendor = data.get("vendor_name")
    if vendor:
        checks.append(
            ValidationCheck(
                rule="Vendor Name Exists",
                status="PASS",
                actual=vendor,
                message="Vendor name is present.",
            )
        )
    else:
        checks.append(
            ValidationCheck(
                rule="Vendor Name Exists",
                status="FAIL",
                message="Vendor name is missing.",
            )
        )

    return checks


def validate_line_items(data: Dict[str, Any]) -> List[ValidationCheck]:
    checks = []
    line_items = data.get("line_items") or []

    for i, item in enumerate(line_items):
        qty_raw = item.get("quantity")
        price_raw = item.get("unit_price")
        amt_raw = item.get("amount")

        if qty_raw is not None and price_raw is not None and amt_raw is not None:
            qty = parse_float(qty_raw)
            price = parse_float(price_raw)
            amt = parse_float(amt_raw)

            expected = qty * price
            # Use math.isclose for robust floating-point comparison
            if math.isclose(expected, amt, abs_tol=TOLERANCE):
                checks.append(
                    ValidationCheck(
                        rule=f"Line Item {i+1} Math",
                        status="PASS",
                        expected=expected,
                        actual=amt,
                        message=f"Line item {i+1} math is correct.",
                    )
                )
            else:
                checks.append(
                    ValidationCheck(
                        rule=f"Line Item {i+1} Math",
                        status="FAIL",
                        expected=expected,
                        actual=amt,
                        message=f"Line item {i+1} math mismatch.",
                    )
                )
        else:
            checks.append(
                ValidationCheck(
                    rule=f"Line Item {i+1} Completeness",
                    status="WARNING",
                    message=f"Line item {i+1} is missing qty, price, or amount for math check.",
                )
            )

    return checks


def validate_subtotal(data: Dict[str, Any]) -> ValidationCheck:
    subtotal_val = data.get("subtotal")
    if subtotal_val is None:
        return ValidationCheck(
            rule="Subtotal Validation", status="WARNING", message="Subtotal is missing."
        )

    subtotal = parse_float(subtotal_val)
    line_items = data.get("line_items") or []

    if not line_items:
        return ValidationCheck(
            rule="Subtotal Validation",
            status="WARNING",
            message="No line items to validate subtotal against.",
        )

    expected_subtotal = sum_line_items(line_items)
    if math.isclose(expected_subtotal, subtotal, abs_tol=TOLERANCE):
        return ValidationCheck(
            rule="Subtotal Validation",
            status="PASS",
            expected=expected_subtotal,
            actual=subtotal,
            message="Subtotal matches line items sum.",
        )

    return ValidationCheck(
        rule="Subtotal Validation",
        status="FAIL",
        expected=expected_subtotal,
        actual=subtotal,
        message="Subtotal does not match line items sum.",
    )


def validate_grand_total(data: Dict[str, Any]) -> ValidationCheck:
    total_val = data.get("total")
    if total_val is None:
        return ValidationCheck(
            rule="Grand Total Validation", status="WARNING", message="Total is missing."
        )

    total = parse_float(total_val)
    subtotal = parse_float(data.get("subtotal"))
    tax = parse_float(data.get("tax"))
    discount = parse_float(data.get("discount"))

    expected_total = calculate_expected_total(subtotal, tax, discount)
    if math.isclose(expected_total, total, abs_tol=TOLERANCE):
        return ValidationCheck(
            rule="Grand Total Validation",
            status="PASS",
            expected=expected_total,
            actual=total,
            message="Grand total math is correct.",
        )

    return ValidationCheck(
        rule="Grand Total Validation",
        status="FAIL",
        expected=expected_total,
        actual=total,
        message="Grand total math mismatch.",
    )
