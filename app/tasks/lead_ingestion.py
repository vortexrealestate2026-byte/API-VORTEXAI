import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger("vortex.tasks.lead_ingestion")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def ingest_leads_task(self):
    """Nightly task to fetch motivated seller leads from BatchData and store them in the DB."""
    try:
        from app.database import SessionLocal
        from app.services.batchdata import BatchDataService

        db = SessionLocal()
        try:
            service = BatchDataService()
            count = service.ingest_leads(db)
            logger.info(f"ingest_leads_task completed: {count} new leads ingested")
            return {"status": "success", "leads_ingested": count}
        finally:
            db.close()
    except Exception as exc:
        logger.error(f"ingest_leads_task failed: {exc}")
        raise self.retry(exc=exc)
