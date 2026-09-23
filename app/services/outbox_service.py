import json
from sqlalchemy.orm import Session
from app.models.privacy import OutboxEvent, AuditTrail, DataSubject
from app.core.security import generate_audit_checksum

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

            now_str = str(db.execute(Session.object_session(subject).text("SELECT CURRENT_TIMESTAMP")).scalar() if hasattr(db, 'execute') else "now")
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
        except Exception:
            db.rollback()
            return None, None
