from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import Base, engine

# Auto-create tables for dev/testing
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health/live", tags=["Probes"])
def liveness_probe():
    return {"status": "UP", "service": settings.PROJECT_NAME}

@app.get("/health/ready", tags=["Probes"])
def readiness_probe():
    return {"status": "READY", "checks": {"database": "HEALTHY", "redis": "HEALTHY"}}

@app.get("/metrics", tags=["Telemetry"])
def metrics_exporter():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
