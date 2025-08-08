from fastapi import APIRouter, Depends, HTTPException # Import FastAPI tools for creating routes, handling dependencies, and returning errors
from sqlalchemy.orm import Session
from app.schemas.health_vital import HealthVitalBase, HealthVitalCreate, HealthVitalUpdate # Import data models (schemas) for health vital API requests and responses
# Import CRUD functions that talk to the database for health vitals
from app.crud.health_vital import ( 
    create_health_vital,
    get_health_vital,
    update_health_vital,
    delete_health_vital,
)
from app.db.database import get_db
router = APIRouter(prefix="/health_vitals", tags=["Health Vitals"])
@router.post("/", response_model=HealthVitalBase)
def create_health_vital_endpoint(
    hv: HealthVitalCreate,
    db: Session = Depends(get_db)
):
    return create_health_vital(db=db, hv=hv)
@router.get("/{hv_id}", response_model=HealthVitalBase)
def read_health_vital(
    hv_id: str,  # The health vital ID from the URL
    db: Session = Depends(get_db)  # Database session
):
    db_hv = get_health_vital(db, hv_id=hv_id)
    if not db_hv:
        raise HTTPException(status_code=404, detail="Health vital not found !!")
    return db_hv
@router.put("/{hv_id}", response_model=HealthVitalBase)
def update_health_vital_endpoint(
    hv_id: str,
    hv: HealthVitalUpdate,
    db: Session = Depends(get_db)
):
    db_hv = get_health_vital(db, hv_id=hv_id)
    if not db_hv:
        raise HTTPException(status_code=404, detail="Health vital not found !!")
    return update_health_vital(db=db, db_hv=db_hv, hv=hv)
@router.delete("/{hv_id}")  # DELETE endpoint to remove a health vital
def delete_health_vital_endpoint(
    hv_id: str,
    db: Session = Depends(get_db)
):
    db_hv = get_health_vital(db, hv_id=hv_id)
    if not db_hv:
        raise HTTPException(status_code=404, detail="Health vital not found !!")
    delete_health_vital(db=db, db_hv=db_hv)
    return {"ok": True} # Return success confirmation
