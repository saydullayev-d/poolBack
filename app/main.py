from fastapi import FastAPI
import asyncio
from models.database import init_db
from api.routers import router as clients_router
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Client Management API")

app.include_router(clients_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

@app.get("/")
def read_root():
    return {"message": "Server is running"}