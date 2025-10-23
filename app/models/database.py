from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models import (  
    Client, Parent, ClientDiagnosis, GroupHistory, Subscription, RenewalHistory,
    ClientGroup, Relation, Diagnosis, Group, SubscriptionTemplate, Contract, Employee, Room, User, Schedule
)
from typing_extensions import AsyncGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.database_url,
    echo=True,
    connect_args={"check_same_thread": False}
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session