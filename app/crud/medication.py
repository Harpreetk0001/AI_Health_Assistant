from sqlalchemy.orm import Session
from uuid import UUID
from app.models.medication import Medication as MedicationModel
from app.schemas.medication import MedicationCreate, MedicationUpdate
def create_medication(db: Session, med: MedicationCreate) -> MedicationModel:
    db_med = MedicationModel(**med.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med
def get_medication(db: Session, med_id: UUID) -> MedicationModel | None:
    return db.query(MedicationModel).filter(MedicationModel.id == med_id).first()
def update_medication(db: Session, med_id: UUID, med: MedicationUpdate) -> MedicationModel | None:
    db_med = db.query(MedicationModel).filter(MedicationModel.id == med_id).first()
    if db_med is None:
        return None
    for field, value in med.model_dump(exclude_unset=True).items():
        setattr(db_med, field, value)
    db.commit()
    db.refresh(db_med)
    return db_med
def delete_medication(db: Session, med_id: UUID) -> bool:
    db_med = db.query(MedicationModel).filter(MedicationModel.id == med_id).first()
    if db_med is None:
        return False
    db.delete(db_med)
    db.commit()
    return True
