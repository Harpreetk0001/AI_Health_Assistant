from pydantic import BaseModel
from datetime import datetime

class DeviceIntegrationBase(BaseModel):
    device_name: str
    device_type: str | None = None
    is_active: bool | None = True

class DeviceIntegrationCreate(DeviceIntegrationBase):
    user_id: str

class DeviceIntegrationUpdate(BaseModel):
    device_name: str | None = None
    device_type: str | None = None
    is_active: bool | None = None

class DeviceIntegration(DeviceIntegrationBase):
    id: str
    user_id: str
    connected_at: datetime | None = None

    class Config:
        orm_mode = True
