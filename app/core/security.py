import hashlib
import hmac

from app.core.config import settings

def generate_audit_checksum(data_subject_id: str, action: str, timestamp_str: str) -> str:
    """Generates tamper-proof HMAC-SHA256 signature for audit integrity."""
    message = f"{data_subject_id}:{action}:{timestamp_str}".encode('utf-8')
    return hmac.new(settings.SECRET_KEY.encode('utf-8'), message, hashlib.sha256).hexdigest()
