from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PIIEvaluationRequest(BaseModel):
    data_subject_id: str = Field(..., example="sub_usr_998877")
    payload: dict[str, Any] = Field(..., example={"email": "alice@amazon.com", "ssn": "123-45-6789", "age": 28})
    strict_mode: bool = Field(default=True)

class PIIFinding(BaseModel):
    field_path: str
    pii_type: str
    confidence_score: float
    masked_value: str

class PIIEvaluationResponse(BaseModel):
    evaluation_id: str
    data_subject_id: str
    has_pii: bool
    findings_count: int
    findings: list[PIIFinding]
    sanitized_payload: dict[str, Any]
    evaluated_at: datetime
    audit_checksum: str | None = None

class ConsentCheckRequest(BaseModel):
    data_subject_id: str
    scope: str = Field(default="MARKETING_ANALYTICS")

class ConsentCheckResponse(BaseModel):
    data_subject_id: str
    allowed: bool
    consent_status: str
    reason: str

