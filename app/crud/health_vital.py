from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models import HealthVitals
from schemas import HealthVitalCreate, HealthVitalOut, HealthVitalUpdate

router = APIRouter(prefix="/health-vitals", tags=["Health Vitals"])

@router.post("/", response_model=HealthVitalOut)
def create_health_vital(vital: HealthVitalCreate, db: Session = Depends(get_db)):
    new_vital = HealthVitals(**vital.dict())
    db.add(new_vital)
    db.commit()
    db.refresh(new_vital)
    return new_vital

@router.get("/", response_model=list[HealthVitalOut])
def get_all_vitals(db: Session = Depends(get_db)):
    return db.query(HealthVitals).all()

@router.get("/{vital_id}", response_model=HealthVitalOut)
def get_vital(vital_id: UUID, db: Session = Depends(get_db)):
    vital = db.query(HealthVitals).filter(HealthVitals.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=404, detail="Health vital not found")
    return vital

@router.put("/{vital_id}", response_model=HealthVitalOut)
def update_vital(vital_id: UUID, update: HealthVitalUpdate, db: Session = Depends(get_db)):
    vital = db.query(HealthVitals).filter(HealthVitals.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=404, detail="Health vital not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(vital, key, value)
    db.commit()
    db.refresh(vital)
    return vital

@router.delete("/{vital_id}")
def delete_vital(vital_id: UUID, db: Session = Depends(get_db)):
    vital = db.query(HealthVitals).filter(HealthVitals.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=404, detail="Health vital not found")
    db.delete(vital)
    db.commit()
    return {"detail": "Health vital deleted"}

