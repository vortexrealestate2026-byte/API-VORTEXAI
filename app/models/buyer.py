from sqlalchemy import Column, Integer, String
from app.database import Base

class Buyer(Base):

    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)
    budget = Column(Integer)
