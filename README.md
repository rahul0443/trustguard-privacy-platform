# 🛡️ TrustGuard Privacy Platform

[![CI/CD Pipeline](https://github.com/rahul0443/trustguard-privacy-platform/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/rahul0443/trustguard-privacy-platform/actions)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade **Data Privacy Governance, PII Classifier & Audit Outbox Control Plane**. Built specifically for Amazon Devices & Services Trust, Privacy, and Accessibility (DSTP) engineering standards to automate data classification, privacy consent enforcement, and tamper-proof audit trails at scale.

---

## 🏗️ Architecture & Data Flow

```mermaid
flowchart TD
    Client[Microservice / Client App] -->|POST /api/v1/privacy/evaluate| API[FastAPI Privacy Gateway]
    
    subgraph Data Governance Engine
        API --> Classifier[Regex PII Classifier & Sanitizer]
        API --> Consent[Consent Enforcement Service]
        API --> Security[HMAC-SHA256 Audit Signer]
    end
    
    subgraph Reliability & Outbox Pattern
        Security --> Outbox[Transactional Outbox Service]
        Outbox -->|Atomic Commit| DB[(PostgreSQL Database)]
        DB --> AuditTable[audit_trails Table]
        DB --> OutboxTable[outbox_events Table]
    end
    
    subgraph Observability
        API --> Metrics[/metrics Prometheus Exporter]
        API --> Health[/health/live & /health/ready Probes]
    end
```

---

## ✨ Key System Features & Engineering Highlights

* **Automated PII Classification & Data Masking:** Evaluates payload JSON schemas for Personally Identifiable Information (SSN, Email, Phone, Credit Cards) and applies deterministic masking (`[REDACTED-SSN]`, `[REDACTED-EMAIL]`).
* **Transactional Outbox Pattern:** Ensures dual-write consistency between relational audit trails and asynchronous message queues without distributed locks.
* **Tamper-Proof Audit Integrity:** Signs every privacy audit entry with HMAC-SHA256 checksum signatures using `(data_subject_id + action + timestamp)` to guarantee non-repudiation.
* **Consent Scope Verification:** Real-time lookup evaluating data subject preferences (`OPT_IN`, `OPT_OUT`, `RESTRICTED`) prior to analytics processing.
* **Operational Excellence (OE):** Prometheus metrics exporter (`/metrics`), Kubernetes liveness/readiness probes, and fully automated PyTest suite.

---

## 📡 API Reference Table

| Method | Endpoint | Description | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/privacy/evaluate` | Evaluates payload for PII & sanitizes | `PIIEvaluationRequest` | `PIIEvaluationResponse` |
| `POST` | `/api/v1/consent/enforce` | Checks data subject consent status | `ConsentCheckRequest` | `ConsentCheckResponse` |
| `GET` | `/health/live` | Liveness Probe | None | `{"status": "UP"}` |
| `GET` | `/health/ready` | Readiness Probe | None | `{"status": "READY"}` |
| `GET` | `/metrics` | Prometheus Metrics Exporter | None | Text Prometheus format |

---

## 🛠️ Local Quickstart with Docker Compose

```bash
# 1. Clone repository
git clone https://github.com/rahul0443/trustguard-privacy-platform.git
cd trustguard-privacy-platform

# 2. Launch FastAPI web app, PostgreSQL, and Redis
docker-compose up --build -d

# 3. Test Liveness Probe
curl http://localhost:8000/health/live
```

---

## 🧪 Running PyTest Suite

```bash
# Install test dependencies
pip install -r requirements.txt

# Execute test suite with coverage
pytest tests/ --cov=app
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
