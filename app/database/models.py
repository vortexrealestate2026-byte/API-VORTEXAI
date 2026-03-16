from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    price = Column(Float)
    arv = Column(Float)
    score = Column(Float)
