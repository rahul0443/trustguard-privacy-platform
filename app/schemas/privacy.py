from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class PIIEvaluationRequest(BaseModel):
    data_subject_id: str = Field(..., example="sub_usr_998877")
    payload: Dict[str, Any] = Field(..., example={"email": "alice@amazon.com", "ssn": "123-45-6789", "age": 28})
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
    findings: List[PIIFinding]
    sanitized_payload: Dict[str, Any]
    evaluated_at: datetime

class ConsentCheckRequest(BaseModel):
    data_subject_id: str
    scope: str = Field(default="MARKETING_ANALYTICS")

class ConsentCheckResponse(BaseModel):
    data_subject_id: str
    allowed: bool
    consent_status: str
    reason: str
