from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "vortex",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.lead_ingestion"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "ingest-leads-nightly": {
            "task": "app.tasks.lead_ingestion.ingest_leads_task",
            "schedule": crontab(hour=2, minute=0),
        },
    },
)
