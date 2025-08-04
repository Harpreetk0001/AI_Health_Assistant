from app.models import DeviceIntegration
from app.db.session import db

def create_device_integration(device_integration):
    db.add(device_integration)
    db.commit()
    db.refresh(device_integration)
    return device_integration

def get_device_integration_by_id(device_integration_id):
    return db.query(DeviceIntegration).filter(DeviceIntegration.id == device_integration_id).first()
