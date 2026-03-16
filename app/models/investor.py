from sqlalchemy import Column, Integer, String
from app.database import Base


class Investor(Base):

    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)
    budget = Column(Integer)
