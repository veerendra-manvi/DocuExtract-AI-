from typing import Any, List, Optional

from pydantic import BaseModel


class ValidationCheck(BaseModel):
    rule: str
    status: str  # PASS, WARNING, FAIL
    expected: Optional[Any] = None
    actual: Optional[Any] = None
    message: str


class ValidationReport(BaseModel):
    status: str
    completeness: float
    checks: List[ValidationCheck]
