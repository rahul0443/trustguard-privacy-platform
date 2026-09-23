import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class DataSubject(Base):
    __tablename__ = "data_subjects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id = Column(String, unique=True, nullable=False, index=True)
    consent_status = Column(String, default="OPT_IN") # OPT_IN, OPT_OUT, RESTRICTED
    region = Column(String, default="US-EAST")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audits = relationship("AuditTrail", back_populates="data_subject")

class AuditTrail(Base):
    __tablename__ = "audit_trails"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    data_subject_id = Column(String, ForeignKey("data_subjects.id"), nullable=False, index=True)
    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    hash_checksum = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    data_subject = relationship("DataSubject", back_populates="audits")

class PIIFindingModel(Base):
    __tablename__ = "pii_findings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id = Column(String, nullable=False, index=True)
    field_path = Column(String, nullable=False)
    pii_type = Column(String, nullable=False) # SSN, EMAIL, PHONE, CREDIT_CARD
    confidence_score = Column(Float, default=0.99)
    masked_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String, nullable=False)
    payload_json = Column(Text, nullable=False)
    status = Column(String, default="PENDING") # PENDING, PROCESSED, FAILED
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
