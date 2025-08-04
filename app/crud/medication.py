from app.models import Medication
from app.db.session import db

def create_medication(medication):
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication

def get_medication_by_id(medication_id):
    return db.query(Medication).filter(Medication.id == medication_id).first()
