
from sqlalchemy import Column, Integer, String
from ..db import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    price = Column(Integer)
