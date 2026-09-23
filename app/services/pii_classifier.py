import re
import uuid
from typing import Dict, Any, List, Tuple
from app.schemas.privacy import PIIFinding

class PIIClassifier:
    """Production PII regex classifier enforcing data privacy classification."""
    
    PATTERNS = {
        "SSN": (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]"),
        "EMAIL": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED-EMAIL]"),
        "PHONE": (r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b", "[REDACTED-PHONE]"),
        "CREDIT_CARD": (r"\b(?:\d[ -]*?){13,16}\b", "[REDACTED-CARD]"),
    }

    def evaluate_payload(self, payload: Dict[str, Any]) -> Tuple[bool, List[PIIFinding], Dict[str, Any]]:
        findings: List[PIIFinding] = []
        sanitized = {}

        for key, val in payload.items():
            if isinstance(val, str):
                matched = False
                current_val = val
                for pii_type, (regex, mask) in self.PATTERNS.items():
                    if re.search(regex, current_val):
                        matched = True
                        findings.append(PIIFinding(
                            field_path=key,
                            pii_type=pii_type,
                            confidence_score=0.99,
                            masked_value=mask
                        ))
                        current_val = re.sub(regex, mask, current_val)
                sanitized[key] = current_val if matched else val
            else:
                sanitized[key] = val

        has_pii = len(findings) > 0
        return has_pii, findings, sanitized
