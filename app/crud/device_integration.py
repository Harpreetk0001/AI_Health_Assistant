from sqlalchemy.orm import Session
from app.models.device_integration import DeviceIntegration
from app.schemas.device_integration import DeviceIntegrationCreate, DeviceIntegrationUpdate
def create_device(db: Session, device: DeviceIntegrationCreate):
    db_device = DeviceIntegration(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeviceIntegration).offset(skip).limit(limit).all()
def get_device(db: Session, device_id: str):
    return db.query(DeviceIntegration).filter(DeviceIntegration.id == device_id).first()
def update_device(db: Session, device_id: str, updates: DeviceIntegrationUpdate):
    db_device = db.query(DeviceIntegration).filter(DeviceIntegration.id == device_id).first()
    if db_device:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_device, field, value)
        db.commit()
        db.refresh(db_device)
    return db_device
def delete_device(db: Session, device_id: str):
    db_device = db.query(DeviceIntegration).filter(DeviceIntegration.id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device
