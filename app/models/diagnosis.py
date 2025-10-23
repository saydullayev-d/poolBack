import uuid
from sqlalchemy import Column, String
from .base import Base

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # e.g., 'Scoliosis'
