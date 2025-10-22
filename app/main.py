from fastapi import FastAPI
from app.core.database import Base, engine
from app.utils.seed_data import create_all
from app.core.database import SessionLocal
from app.core.health_monitoring_core import load_vitals_from_db
from app.routers import auth, vitals, tasks, contacts, ml

# create tables if missing
create_all()

app = FastAPI(title="MedBuddy Backend")

# include routers
app.include_router(auth.router)
app.include_router(vitals.router)
app.include_router(tasks.router)
app.include_router(contacts.router)
app.include_router(ml.router)

@app.on_event("startup")
def startup_event():
    # load vitals into memory
    db = SessionLocal()
    try:
        load_vitals_from_db(db)
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}
