import logging
import os

from fastapi import (APIRouter, BackgroundTasks, File, HTTPException, Request,
                     UploadFile, status)

from app.services.file_service import UPLOAD_DIR, process_upload
from app.services.pipeline.document_pipeline import process_document_pipeline

logger = logging.getLogger(__name__)

router = APIRouter()


def remove_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Cleaned up file: {path}")
    except Exception as e:
        logger.error(f"Failed to clean up file {path}: {e}")


@router.post("/extract")
async def extract_document(
    request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    """
    Upload a document and execute the complete AI extraction pipeline.
    Supported types: PDF, PNG, JPG, JPEG, TXT
    Max file size: 20 MB
    """
    logger.info("--- Incoming Request Debug ---")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Uploaded Filename: {file.filename}")
    logger.info(f"Content-Type: {file.content_type}")
    logger.info("------------------------------")
    # 1. Process secure file upload (Validates size, type, handles 400, 413, 500)
    upload_response = process_upload(file)

    file_path = UPLOAD_DIR / upload_response.stored_filename

    # Schedule cleanup task
    background_tasks.add_task(remove_file, str(file_path))

    # 2. Execute full Document Processing Pipeline (async)
    pipeline_result = await process_document_pipeline(
        file_path=str(file_path), original_filename=upload_response.original_filename
    )

    # 3. Handle Pipeline Result (422 on logic failure, 200 on success)
    if not pipeline_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": pipeline_result.get("error"),
                "details": pipeline_result.get("details"),
                "metadata": pipeline_result.get("metadata"),
            },
        )

    return pipeline_result
