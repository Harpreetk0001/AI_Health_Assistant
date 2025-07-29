# main.py

from fastapi import FastAPI
from app.api.endpoints import health
from app.db.base import Base
from app.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router, prefix="/api", tags=["health"])
