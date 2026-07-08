import logging
import time
from typing import Any, Dict

from app.services.ai.extractor import extract_structured_data
from app.services.intelligence.classifier import classify_document
from app.services.intelligence.cleaner import clean_text
from app.services.parsers.extractor import extract_document_text
from app.services.validation.validator import generate_validation_report

logger = logging.getLogger(__name__)


async def process_document_pipeline(
    file_path: str, original_filename: str
) -> Dict[str, Any]:
    """
    Orchestrates the entire end-to-end document processing pipeline.
    """
    start_time = time.time()

    try:
        # 1 & 2 & 3. Extract raw text via File Service / Parsers
        logger.info(f"Pipeline Step 1: Extracting text from {original_filename}")
        extraction_result = await extract_document_text(file_path)
        raw_text = extraction_result.get("text", "")
        file_ext_type = extraction_result.get("document_type", "unknown")

        if not raw_text.strip() or len(raw_text.strip()) < 30:
            return _build_error_response(
                "Failed to extract sufficient readable text from the document (less than 30 characters).",
                start_time,
            )

        # 4. Clean extracted text
        logger.info("Pipeline Step 2: Cleaning text")
        cleaned_text = clean_text(raw_text)

        logger.info("--- COMPLETE OCR TEXT ---")
        logger.info(f"\n{cleaned_text}\n")
        logger.info("-------------------------")

        # 5. Detect document type deterministically
        logger.info("Pipeline Step 3: Classifying document type")
        classification = classify_document(cleaned_text)
        doc_type_detected = classification["document_type"]
        confidence = classification["confidence"]

        # 6 & 7. Send to AI Extraction Engine (Includes Output Parsing)
        logger.info("Pipeline Step 4: AI Extraction Engine")
        ai_result = await extract_structured_data(cleaned_text)

        if ai_result.get("status") != "success":
            return _build_error_response(
                f"AI Extraction Failed: {ai_result.get('error')}",
                start_time,
                details=ai_result.get("details"),
            )

        extracted_data = ai_result["extracted_data"]
        ai_metadata = ai_result["metadata"]

        # Merge deterministic doc_type if AI missed it or guessed "unknown"
        if (
            not extracted_data.get("document_type")
            or extracted_data.get("document_type") == "unknown"
        ):
            extracted_data["document_type"] = doc_type_detected

        # 8. Validate extracted document
        logger.info("Pipeline Step 5: Rule-Based Validation")
        validation_report = generate_validation_report(extracted_data)
        logger.info("--- VALIDATION RESULTS ---")
        import json

        logger.info(json.dumps(validation_report.model_dump(), indent=2))
        logger.info("--------------------------")

        # 9. Generate final ProcessingResult response
        processing_time_ms = int((time.time() - start_time) * 1000)

        return {
            "success": True,
            "document": extracted_data,
            "validation": validation_report.model_dump(),
            "metadata": {
                "document_type": extracted_data.get("document_type", "unknown"),
                "provider": ai_metadata.get("provider", "unknown"),
                "processing_time_ms": processing_time_ms,
                "file_name": original_filename,
                "pages": 1,
                "ocr_used": file_ext_type == "image",
                "confidence": confidence,
            },
        }

    except Exception as e:
        logger.error(f"Pipeline crashed entirely: {e}")
        return _build_error_response(
            f"Pipeline crashed unexpectedly: {str(e)}", start_time
        )


def _build_error_response(
    message: str, start_time: float, details: str = None
) -> Dict[str, Any]:
    processing_time_ms = int((time.time() - start_time) * 1000)
    return {
        "success": False,
        "error": message,
        "details": details,
        "metadata": {"processing_time_ms": processing_time_ms},
    }
