import uuid
from sqlalchemy import Column, String, Numeric, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from app.models.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False, index=True)
    owner_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    estimated_equity = Column(Numeric(12, 2), nullable=True)
    distress_type = Column(
        Enum("pre_foreclosure", "absentee_owner", "tax_lien", name="distress_type_enum"),
        nullable=False,
    )
    arv = Column(Numeric(12, 2), nullable=True)
    suggested_offer = Column(Numeric(12, 2), nullable=True)
    status = Column(
        Enum("new", "analyzed", "contract_sent", "signed", "closed", "dead", name="lead_status_enum"),
        nullable=False,
        default="new",
    )
    batchdata_id = Column(String, unique=True, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
