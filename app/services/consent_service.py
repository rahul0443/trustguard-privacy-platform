import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.privacy import DataSubject
from app.schemas.privacy import ConsentCheckResponse

logger = logging.getLogger(__name__)

class ConsentService:
    def check_consent(self, db: Session, data_subject_id: str, scope: str) -> ConsentCheckResponse:
        subject = db.query(DataSubject).filter(DataSubject.external_id == data_subject_id).first()

        if not subject:
            # Create default data subject record
            subject = DataSubject(external_id=data_subject_id, consent_status="OPT_IN")
            try:
                db.add(subject)
                db.commit()
                db.refresh(subject)
            except SQLAlchemyError:
                logger.warning("Failed to persist new data subject %s", data_subject_id, exc_info=True)
                db.rollback()

        status = subject.consent_status if subject else "OPT_IN"
        allowed = status == "OPT_IN"
        reason = "Subject consent active" if allowed else f"Consent status is {status}"

        return ConsentCheckResponse(
            data_subject_id=data_subject_id,
            allowed=allowed,
            consent_status=status,
            reason=reason
        )
