import logging
from datetime import UTC, datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import generate_audit_checksum
from app.models.privacy import AuditTrail, DataSubject, OutboxEvent

logger = logging.getLogger(__name__)

class OutboxService:
    """Implements Transactional Outbox Pattern to ensure reliable audit logging."""

    def record_audit_and_outbox(
        self, db: Session, external_subject_id: str, action: str, payload_json: str
    ):
        try:
            subject = db.query(DataSubject).filter(DataSubject.external_id == external_subject_id).first()
            if not subject:
                subject = DataSubject(external_id=external_subject_id, consent_status="OPT_IN")
                db.add(subject)
                db.flush()

            now_str = datetime.now(UTC).isoformat()
            checksum = generate_audit_checksum(subject.id, action, now_str)

            audit = AuditTrail(
                data_subject_id=subject.id,
                action=action,
                ip_address="127.0.0.1",
                hash_checksum=checksum
            )
            outbox = OutboxEvent(
                event_type=f"PRIVACY_AUDIT_{action.upper()}",
                payload_json=payload_json,
                status="PENDING"
            )

            db.add(audit)
            db.add(outbox)
            db.commit()
            return audit, outbox
        except SQLAlchemyError:
            logger.warning("Failed to record audit/outbox event for %s", external_subject_id, exc_info=True)
            db.rollback()
            return None, None
