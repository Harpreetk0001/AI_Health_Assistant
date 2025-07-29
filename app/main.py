from fastapi import FastAPI
from app.api.endpoints import health
from app.db.session import engine
from app.db import base  # Import to create tables

base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Health Assistant Backend")

app.include_router(health.router, prefix="/health", tags=["Health Data"])
