from fastapi import FastAPI
import asyncio
from app.models.database import init_db
from app.api.routes.clients import router as clients_router
from app.api.routes.diagnoses import router as diagnoses_router
from app.api.routes.groups import router as group_router
from app.api.routes.relations import router as relations_router
from app.api.routes.subscription_templates import router as subscription_template_router
from app.api.routes.contract import router as contract_router
from app.api.routes.employee import router as employee_router
from app.api.routes.room import router as room_router
from app.api.routes.schedule import router as schedule_router
from app.api.routes.subscription import router as subscription_router
from app.api.routes.users import router as user_router
from contextlib import asynccontextmanager
from app.models import (  
    Client, Parent, ClientDiagnosis, GroupHistory, Subscription, RenewalHistory,
    ClientGroup, Relation, Diagnosis, Group, SubscriptionTemplate, Contract, Employee, Room, User, Schedule
)
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # выполняется при запуске приложения
    await init_db()
    print("Database initialized successfully")
    
    yield  # здесь работает само приложение

    # выполняется при завершении приложения
    print("Application shutting down")

app = FastAPI(title="Client Management API", lifespan=lifespan)

app.include_router(clients_router)
app.include_router(diagnoses_router)
app.include_router(group_router)
app.include_router(relations_router)
app.include_router(subscription_template_router)
app.include_router(contract_router)
app.include_router(employee_router)
app.include_router(room_router)
app.include_router(schedule_router)
app.include_router(subscription_router)
app.include_router(user_router)

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