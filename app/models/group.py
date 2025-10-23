import uuid
from sqlalchemy import Column, String
from .base import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
