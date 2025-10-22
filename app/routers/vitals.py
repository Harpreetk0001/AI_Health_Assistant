from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.utils.dependencies import get_db, get_current_user
from app.core.health_monitoring_core import Vitals as VitalsObj

router = APIRouter(prefix="/vitals", tags=["vitals"])

@router.post("/", response_model=schemas.VitalsOut)
def create_vitals(vitals: schemas.VitalsIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_v = crud.create_vitals(db, current_user.id, vitals)
    # add to in-memory matrices
    VitalsObj(
        hydration=db_v.hydration,
        sleep=db_v.sleep,
        hb=db_v.heartbeat,
        bp_systolic=db_v.bp_systolic,
        bp_diastolic=db_v.bp_diastolic,
        steps=db_v.steps,
        timestamp=db_v.timestamp
    )
    return db_v

@router.get("/", response_model=List[schemas.VitalsOut])
def read_vitals(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_vitals_for_user(db, current_user.id)
