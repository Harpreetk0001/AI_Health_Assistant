from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
class DeviceIntegrationBase(BaseModel):
    user_id: UUID
    device_name: str
    integration_status: str
class DeviceIntegrationCreate(DeviceIntegrationBase):
    pass
class DeviceIntegrationUpdate(BaseModel):
    device_name: str
    integration_status: str
class DeviceIntegrationResponse(DeviceIntegrationBase):
    id: UUID
    integrated_at: datetime
    class Config:
        orm_mode = True
