from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
import crud.device_integration as crud
import schemas.device_integration as schemas

router = APIRouter(prefix="/device_integrations", tags=["Device Integrations"])

@router.post("/", response_model=schemas.DeviceIntegration)
def create_device_integration(device: schemas.DeviceIntegrationCreate, db: Session = Depends(get_db)):
    return crud.create_device_integration(db=db, device=device)

@router.get("/", response_model=list[schemas.DeviceIntegration])
def read_device_integrations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_device_integrations(db=db, skip=skip, limit=limit)

@router.get("/{device_id}", response_model=schemas.DeviceIntegration)
def read_device_integration(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device_integration(db, device_id=device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device integration not found")
    return db_device

@router.put("/{device_id}", response_model=schemas.DeviceIntegration)
def update_device_integration(device_id: int, device: schemas.DeviceIntegrationUpdate, db: Session = Depends(get_db)):
    return crud.update_device_integration(db, device_id=device_id, device=device)

@router.delete("/{device_id}")
def delete_device_integration(device_id: int, db: Session = Depends(get_db)):
    crud.delete_device_integration(db, device_id=device_id)
    return {"ok": True}
