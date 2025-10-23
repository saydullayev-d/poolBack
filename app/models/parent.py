import uuid
from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Parent(Base):
    __tablename__ = "parents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relation_id = Column(String, ForeignKey("relations.id"), nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
