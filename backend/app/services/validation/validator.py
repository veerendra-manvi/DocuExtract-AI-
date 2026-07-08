import logging
from typing import Any, Dict

from app.services.validation.calculators import calculate_completeness
from app.services.validation.report import ValidationCheck, ValidationReport
from app.services.validation.rules import (validate_currency, validate_dates,
                                           validate_grand_total,
                                           validate_invoice_fields,
                                           validate_line_items,
                                           validate_subtotal)

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "document_type",
    "invoice_number",
    "vendor_name",
    "total",
    "currency",
]


def generate_validation_report(data: Dict[str, Any]) -> ValidationReport:
    """
    Runs all deterministic rules and generates a structured validation report.
    """
    logger.info("Starting validation engine.")
    checks = []

    try:
        doc_type = str(data.get("document_type", "")).lower()

        # 1. Date Validation
        checks.extend(validate_dates(data))

        # 2. Currency Validation
        checks.append(validate_currency(data))

        # 3. Invoice Specific Validation
        if doc_type == "invoice":
            checks.extend(validate_invoice_fields(data))

        # 4. Line Items Validation
        checks.extend(validate_line_items(data))

        # 5. Subtotal Validation
        checks.append(validate_subtotal(data))

        # 6. Grand Total Validation
        checks.append(validate_grand_total(data))

    except Exception as e:
        logger.error(f"Error during rule execution: {e}")
        checks.append(
            ValidationCheck(
                rule="Engine Execution",
                status="FAIL",
                message=f"Validation engine crashed: {str(e)}",
            )
        )

    completeness = calculate_completeness(data, REQUIRED_FIELDS)

    status = "PASS"
    for check in checks:
        if check.status == "FAIL":
            status = "FAIL"
            break
        elif check.status == "WARNING" and status == "PASS":
            status = "WARNING"

    return ValidationReport(status=status, completeness=completeness, checks=checks)
