from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///clients.db"

    def __post_init__(self):
        logger.info(f"Using database URL: {self.database_url}")

settings = Settings()