from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root_serves_interactive_sandbox():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "TrustGuard" in response.text

def test_liveness_probe():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_readiness_probe():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "READY"

def test_metrics_exporter():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "trustguard_" in response.text

def test_evaluate_pii_payload():
    payload = {
        "data_subject_id": "sub_test_001",
        "payload": {
            "name": "John Doe",
            "email": "johndoe@amazon.com",
            "ssn": "123-45-6789",
            "score": 95
        }
    }
    response = client.post("/api/v1/privacy/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["has_pii"] is True
    assert data["findings_count"] == 2
    assert "[REDACTED-EMAIL]" in data["sanitized_payload"]["email"]
    assert "[REDACTED-SSN]" in data["sanitized_payload"]["ssn"]
    assert data["audit_checksum"] is not None
    assert len(data["audit_checksum"]) == 64  # HMAC-SHA256 hex digest

def test_enforce_consent():
    payload = {
        "data_subject_id": "sub_test_001",
        "scope": "ANALYTICS"
    }
    response = client.post("/api/v1/consent/enforce", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True
    assert data["consent_status"] == "OPT_IN"
