from fastapi import APIRouter, Depends, HTTPException # Import FastAPI tools for creating routes, using dependencies, and handling errors
from sqlalchemy.orm import Session # Import database session type from SQLAlchemy
from typing import List # Import List type hint for specifying return values
from uuid import UUID # Import UUID type for device IDs
from app.db.session import get_db # Import function to get a database connection
from app.crud import device_integration as crud
from app.schemas import device_integration as schemas
router = APIRouter(prefix="/device_integrations", tags=["Device Integrations"])
@router.post("/", response_model=schemas.DeviceIntegrationBase)
def create_device_integration(
    device: schemas.DeviceIntegrationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_device(db=db, device=device) # Call CRUD function to save the device into the database
@router.get("/", response_model=List[schemas.DeviceIntegrationBase])
def read_device_integrations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_devices(db=db, skip=skip, limit=limit) # Call CRUD function to fetch devices from the database
@router.get("/{device_id}", response_model=schemas.DeviceIntegrationBase)
def read_device_integration(
    device_id: UUID,
    db: Session = Depends(get_db)
):
    db_device = crud.get_device(db, device_id=str(device_id))
    if not db_device:
        raise HTTPException(status_code=404, detail="Device integration not found !!")
    return db_device
@router.put("/{device_id}", response_model=schemas.DeviceIntegrationBase) # Route for updating an existing device integration
def update_device_integration(
    device_id: UUID,
    device: schemas.DeviceIntegrationUpdate,
    db: Session = Depends(get_db)
):
    updated_device = crud.update_device(db, device_id=str(device_id), updates=device)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device integration not found !!")
    return updated_device
@router.delete("/{device_id}")
def delete_device_integration(
    device_id: UUID,
    db: Session = Depends(get_db)
):
    deleted_device = crud.delete_device(db, device_id=str(device_id))
    if not deleted_device:
        raise HTTPException(status_code=404, detail="Device integration not found !!")
    return {"ok": True}
