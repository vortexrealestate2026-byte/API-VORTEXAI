import logging
from typing import Optional, Any

from sqlalchemy.orm import Session

from app.models.log import Log

logger = logging.getLogger("vortex")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def log_event(
    db: Session,
    level: str,
    service: str,
    message: str,
    details: Optional[Any] = None,
) -> None:
    """Insert a log entry into the database and also log to Python logging."""
    log_fn = {
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
        "critical": logger.critical,
    }.get(level, logger.info)

    log_fn(f"[{service}] {message}" + (f" | details={details}" if details else ""))

    try:
        entry = Log(
            level=level,
            service=service,
            message=message,
            details=details,
        )
        db.add(entry)
        db.commit()
    except Exception as exc:
        logger.error(f"Failed to persist log entry to DB: {exc}")
        db.rollback()
