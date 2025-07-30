from sqlalchemy.orm import Session
from app.models.health import HealthRecord
from app.models.emergency_contact import EmergencyContact
from app.schemas.health import HealthRecordCreate

def create_health_record(db: Session, health: HealthRecordCreate):
    db_health = HealthRecord(name=health.name, dob=health.dob)
    db.add(db_health)
    db.commit()
    db.refresh(db_health)

    # Add emergency contacts if provided
    for contact in health.emergency_contacts:
        db_contact = EmergencyContact(
            name=contact.name,
            phone=contact.phone,
            health_record_id=db_health.id
        )
        db.add(db_contact)
    db.commit()
    return db_health

def get_health_records(db: Session, skip: int = 0, limit: int = 10):
    return db.query(HealthRecord).offset(skip).limit(limit).all()
