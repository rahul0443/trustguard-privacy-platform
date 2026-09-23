import json
import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.metrics import CONSENT_ENFORCE_COUNTER, PII_EVALUATION_COUNTER, PII_FINDINGS_COUNTER
from app.db.session import get_db
from app.schemas.privacy import (
    ConsentCheckRequest,
    ConsentCheckResponse,
    PIIEvaluationRequest,
    PIIEvaluationResponse,
)
from app.services.consent_service import ConsentService
from app.services.outbox_service import OutboxService
from app.services.pii_classifier import PIIClassifier

router = APIRouter()
classifier = PIIClassifier()
consent_service = ConsentService()
outbox_service = OutboxService()

@router.post("/privacy/evaluate", response_model=PIIEvaluationResponse, status_code=status.HTTP_200_OK)
def evaluate_privacy_payload(request: PIIEvaluationRequest, db: Annotated[Session, Depends(get_db)]):
    has_pii, findings, sanitized = classifier.evaluate_payload(request.payload)
    
    PII_EVALUATION_COUNTER.labels(status="SUCCESS").inc()
    for f in findings:
        PII_FINDINGS_COUNTER.labels(pii_type=f.pii_type).inc()

    eval_id = f"eval_{uuid.uuid4().hex[:12]}"
    
    # Audit log via Transactional Outbox Pattern
    outbox_service.record_audit_and_outbox(
        db,
        external_subject_id=request.data_subject_id,
        action="PII_EVALUATION",
        payload_json=json.dumps({"has_pii": has_pii, "findings_count": len(findings)})
    )

    return PIIEvaluationResponse(
        evaluation_id=eval_id,
        data_subject_id=request.data_subject_id,
        has_pii=has_pii,
        findings_count=len(findings),
        findings=findings,
        sanitized_payload=sanitized,
        evaluated_at=datetime.now(UTC)
    )

@router.post("/consent/enforce", response_model=ConsentCheckResponse, status_code=status.HTTP_200_OK)
def enforce_consent(request: ConsentCheckRequest, db: Annotated[Session, Depends(get_db)]):
    result = consent_service.check_consent(db, request.data_subject_id, request.scope)
    decision = "ALLOWED" if result.allowed else "BLOCKED"
    CONSENT_ENFORCE_COUNTER.labels(decision=decision).inc()
    return result
