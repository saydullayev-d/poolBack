import uuid
from sqlalchemy import Column, String
from .base import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
