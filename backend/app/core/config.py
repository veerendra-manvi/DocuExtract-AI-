from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "DocuExtract AI"
    PROJECT_DESCRIPTION: str = (
        "AI-powered document data extractor for invoices, receipts, and purchase orders."
    )
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Provider settings
    LLM_PROVIDER: str = "openai"  # or "groq"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
