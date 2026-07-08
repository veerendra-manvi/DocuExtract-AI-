import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)

INVOICE_KEYWORDS = [
    "invoice",
    "tax invoice",
    "bill to",
    "invoice number",
    "amount due",
    "balance due",
    "subtotal",
]
RECEIPT_KEYWORDS = [
    "receipt",
    "paid",
    "cash",
    "change",
    "merchant",
    "card ending in",
    "transaction",
]
PO_KEYWORDS = [
    "purchase order",
    "po number",
    "supplier",
    "ship to",
    "vendor",
    "purchase order number",
]

# Pre-compile word boundary regexes for highly accurate matching
INVOICE_REGEXES = [re.compile(rf"\b{re.escape(kw)}\b") for kw in INVOICE_KEYWORDS]
RECEIPT_REGEXES = [re.compile(rf"\b{re.escape(kw)}\b") for kw in RECEIPT_KEYWORDS]
PO_REGEXES = [re.compile(rf"\b{re.escape(kw)}\b") for kw in PO_KEYWORDS]


def classify_document(text: str) -> Dict[str, Any]:
    """
    Classifies a document based on deterministic keyword heuristics using exact word boundaries.
    Returns the document type and a confidence score.
    """
    if not text:
        return {"document_type": "unknown", "confidence": 0.0}

    text_lower = text.lower()

    invoice_score = sum(1 for pattern in INVOICE_REGEXES if pattern.search(text_lower))
    receipt_score = sum(1 for pattern in RECEIPT_REGEXES if pattern.search(text_lower))
    po_score = sum(1 for pattern in PO_REGEXES if pattern.search(text_lower))

    scores = {
        "invoice": invoice_score,
        "receipt": receipt_score,
        "purchase_order": po_score,
    }

    max_type = max(scores, key=scores.get)
    max_score = scores[max_type]

    if max_score == 0:
        return {"document_type": "unknown", "confidence": 0.0}

    # Simple heuristic confidence
    # Total distinct matching keywords * weight, capped at 0.98 for heuristic logic
    confidence = min(0.98, max_score * 0.25)

    return {"document_type": max_type, "confidence": round(confidence, 2)}
