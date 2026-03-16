from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String)

    city = Column(String, index=True)
    state = Column(String)

    price = Column(Float)
    arv = Column(Float)  # After Repair Value
    estimated_repair = Column(Float)

    property_type = Column(String)
    source = Column(String)  # Zillow, Redfin, etc.

    status = Column(String, default="new")  
    # new / under_contract / sold

    contact_name = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
