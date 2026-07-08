from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    file_id: str
    original_filename: str
    stored_filename: str
    content_type: str
    file_size: int
    upload_time: datetime
    status: str
