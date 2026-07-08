import logging
from typing import Any, Dict

from app.services.ai.parser import parse_ai_response
from app.services.ai.prompts import SYSTEM_PROMPT, build_extraction_prompt
from app.services.ai.provider import AIProvider

logger = logging.getLogger(__name__)


async def extract_structured_data(clean_text: str) -> Dict[str, Any]:
    """
    Orchestrates the AI extraction with exactly 1 automatic retry on JSON failure.
    Dynamically adjusts temperature on retry to prevent deterministic failure loops.
    """
    provider = AIProvider()
    user_prompt = build_extraction_prompt(clean_text)

    max_retries = 1
    attempts = 0

    while attempts <= max_retries:
        attempts += 1

        # Slightly bump temperature on retries to break out of deterministic bad-JSON loops
        temp = 0.0 if attempts == 1 else 0.3

        try:
            raw_response, metrics = await provider.generate_json(
                SYSTEM_PROMPT, user_prompt, temperature=temp
            )

            logger.info("--- AI PROMPT SENT ---")
            logger.info(user_prompt)
            logger.info("----------------------")

            logger.info("--- RAW AI RESPONSE ---")
            logger.info(raw_response)
            logger.info("-----------------------")

            parsed_data = parse_ai_response(raw_response)

            logger.info("--- PARSED JSON ---")
            import json

            logger.info(json.dumps(parsed_data, indent=2))
            logger.info("-------------------")

            logger.info(
                f"AI Extraction successful | Provider: {metrics['provider']} | "
                f"Time: {metrics['execution_time_sec']}s | "
                f"Tokens: {metrics['usage']} | Attempts: {attempts}"
            )

            return {
                "status": "success",
                "extracted_data": parsed_data,
                "metadata": metrics,
            }

        except ValueError as e:
            logger.warning(f"JSON parsing failed on attempt {attempts}: {e}")
            if attempts > max_retries:
                logger.error("Max retries reached for JSON parsing.")
                return {
                    "status": "error",
                    "error": "Failed to parse structured data after retries.",
                    "details": str(e),
                }
        except RuntimeError as e:
            logger.error(f"AI extraction failed on attempt {attempts}: {e}")
            if attempts > max_retries:
                return {
                    "status": "error",
                    "error": "AI Provider error.",
                    "details": str(e),
                }
        except Exception as e:
            logger.error(f"Unexpected extraction orchestrator error: {e}")
            return {"status": "error", "error": "Unknown failure", "details": str(e)}

    return {"status": "error", "error": "Exceeded retry loop inexplicably"}
