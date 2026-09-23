from prometheus_client import Counter, Histogram

PII_EVALUATION_COUNTER = Counter(
    "trustguard_pii_evaluations_total",
    "Total PII classifications performed",
    ["status"]
)

PII_FINDINGS_COUNTER = Counter(
    "trustguard_pii_findings_total",
    "Total PII elements detected by category",
    ["pii_type"]
)

CONSENT_ENFORCE_COUNTER = Counter(
    "trustguard_consent_enforcement_total",
    "Total consent verification checks",
    ["decision"]
)

EVALUATION_LATENCY_HISTOGRAM = Histogram(
    "trustguard_evaluation_latency_seconds",
    "Latency of PII evaluation in seconds",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)
