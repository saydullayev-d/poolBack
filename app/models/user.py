import uuid
from sqlalchemy import Column, String
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
