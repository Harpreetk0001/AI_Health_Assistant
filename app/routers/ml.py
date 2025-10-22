from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.utils.dependencies import get_db, get_current_user
from app.ml.symptom_analyzer import analyze_symptoms

router = APIRouter(prefix="/ml", tags=["ml"])

@router.post("/analyze")
def ml_analyze(payload: schemas.MLResultIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    predicted = analyze_symptoms(payload.symptom_input)
    crud.save_ml_result(db, current_user.id, payload.symptom_input, predicted)
    return {"prediction": predicted}
