from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user
from app.database import get_db
from app.models.log import Log
from app.models.user import User

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("")
def list_logs(
    level: Optional[str] = Query(None, description="Filter by log level: info, warning, error, critical"),
    service: Optional[str] = Query(None, description="Filter by service name"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    query = db.query(Log)
    if level:
        query = query.filter(Log.level == level)
    if service:
        query = query.filter(Log.service == service)
    logs = query.order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": str(log.id),
            "level": log.level,
            "service": log.service,
            "message": log.message,
            "details": log.details,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
