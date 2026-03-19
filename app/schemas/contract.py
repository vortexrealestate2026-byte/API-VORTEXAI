from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID

from pydantic import BaseModel


class ContractOut(BaseModel):
    id: UUID
    lead_id: UUID
    docusign_envelope_id: str
    status: str
    sent_at: Optional[datetime] = None
    signed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocuSignWebhookPayload(BaseModel):
    envelopeId: Optional[str] = None
    status: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}
