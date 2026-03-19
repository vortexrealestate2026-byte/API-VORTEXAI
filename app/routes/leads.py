from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user, get_current_user
from app.core.logging import log_event
from app.database import get_db
from app.models.lead import Lead
from app.models.user import User
from app.schemas.lead import DealAnalysis, LeadOut, LeadUpdate
from app.services.housecanary import HouseCanaryService
from app.services.docusign import DocuSignService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=List[LeadOut])
def list_leads(
    status: Optional[str] = Query(None),
    distress_type: Optional[str] = Query(None),
    zip_code: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    if distress_type:
        query = query.filter(Lead.distress_type == distress_type)
    if zip_code:
        query = query.filter(Lead.zip_code == zip_code)
    return query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/analyze/{lead_id}", response_model=DealAnalysis)
def analyze_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    hc = HouseCanaryService()
    try:
        analysis = hc.analyze_deal(lead.address, lead.zip_code)
    except Exception as exc:
        log_event(db, "error", "housecanary", f"analyze_deal failed for lead {lead_id}: {exc}")
        raise HTTPException(status_code=502, detail=f"HouseCanary API error: {exc}")

    if analysis.get("arv"):
        lead.arv = analysis["arv"]
    if analysis.get("suggested_offer"):
        lead.suggested_offer = analysis["suggested_offer"]
    lead.status = "analyzed"
    db.commit()

    log_event(db, "info", "housecanary", f"Deal analyzed for lead {lead_id}", details={"arv": str(analysis.get("arv"))})
    return analysis


@router.post("/{lead_id}/send-contract")
def send_contract(
    lead_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if not lead.suggested_offer:
        raise HTTPException(status_code=400, detail="Lead must be analyzed before sending contract")

    docusign = DocuSignService()
    try:
        envelope_id = docusign.send_contract(lead, db)
    except Exception as exc:
        log_event(db, "error", "docusign", f"send_contract failed for lead {lead_id}: {exc}")
        raise HTTPException(status_code=502, detail=f"DocuSign error: {exc}")

    log_event(db, "info", "docusign", f"Contract sent for lead {lead_id}, envelope={envelope_id}")
    return {"lead_id": str(lead_id), "envelope_id": envelope_id, "status": "sent"}


@router.post("/ingest")
def trigger_ingest(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    from app.tasks.lead_ingestion import ingest_leads_task
    task = ingest_leads_task.delay()
    log_event(db, "info", "batchdata", f"Manual lead ingest triggered, task_id={task.id}")
    return {"status": "queued", "task_id": task.id}
