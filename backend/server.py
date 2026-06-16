from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase connection (replaces MongoDB)
supabase: Client = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_SERVICE_KEY']
)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.model_dump())

    # Map model fields to Supabase table columns
    doc = {
        "id": status_obj.id,
        "client_name": status_obj.client_name,
        "created_at": status_obj.timestamp.isoformat(),
    }

    supabase.table("status_checks").insert(doc).execute()
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    result = supabase.table("status_checks").select("*").limit(1000).execute()

    checks = []
    for row in result.data:
        # Map created_at from Supabase back to timestamp for the model
        raw_ts = row.get("created_at", "")
        if isinstance(raw_ts, str):
            raw_ts = raw_ts.replace("Z", "+00:00")
            parsed_ts = datetime.fromisoformat(raw_ts)
        else:
            parsed_ts = datetime.now(timezone.utc)

        checks.append(StatusCheck(
            id=row["id"],
            client_name=row["client_name"],
            timestamp=parsed_ts,
        ))

    return checks


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# No shutdown hook needed — Supabase client doesn't hold open connections