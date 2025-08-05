from sqlalchemy.orm import Session
from models import medication as models
from schemas import medication as schemas

def create_medication(db: Session, medication: schemas.MedicationCreate):
    db_med = models.Medication(**medication.dict())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med

def get_medications(db: Session, skip=0, limit=100):
    return db.query(models.Medication).offset(skip).limit(limit).all()

def get_medication(db: Session, med_id: str):
    return db.query(models.Medication).filter(models.Medication.id == med_id).first()

def update_medication(db: Session, med_id: str, updates: schemas.MedicationUpdate):
    db_med = db.query(models.Medication).filter(models.Medication.id == med_id).first()
    if db_med:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_med, field, value)
        db.commit()
        db.refresh(db_med)
    return db_med

def delete_medication(db: Session, med_id: str):
    db_med = db.query(models.Medication).filter(models.Medication.id == med_id).first()
    if db_med:
        db.delete(db_med)
        db.commit()
    return db_med
