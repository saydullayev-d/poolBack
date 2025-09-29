import uuid
from sqlalchemy import Column, String
from .base import Base

class Relation(Base):
    __tablename__ = "relations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # e.g., 'Mother'
