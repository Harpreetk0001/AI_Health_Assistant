from sqlalchemy.orm import Session
from models import device_integration as models
from schemas import device_integration as schemas

def create_device(db: Session, device: schemas.DeviceIntegrationCreate):
    db_device = models.DeviceIntegration(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session, skip=0, limit=100):
    return db.query(models.DeviceIntegration).offset(skip).limit(limit).all()

def get_device(db: Session, device_id: str):
    return db.query(models.DeviceIntegration).filter(models.DeviceIntegration.id == device_id).first()

def update_device(db: Session, device_id: str, updates: schemas.DeviceIntegrationUpdate):
    db_device = db.query(models.DeviceIntegration).filter(models.DeviceIntegration.id == device_id).first()
    if db_device:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_device, field, value)
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: str):
    db_device = db.query(models.DeviceIntegration).filter(models.DeviceIntegration.id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device
