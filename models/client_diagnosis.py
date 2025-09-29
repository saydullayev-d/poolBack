import uuid
from sqlalchemy import Column, String, ForeignKey
from .base import Base

class ClientDiagnosis(Base):
    __tablename__ = "client_diagnoses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    diagnosis_id = Column(String, ForeignKey("diagnoses.id"), nullable=False)
    notes = Column(String, nullable=True)
