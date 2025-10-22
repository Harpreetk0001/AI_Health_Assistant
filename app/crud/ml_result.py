from sqlalchemy.orm import Session
from app.models.ml_result import MLResult

def save_ml_result(db: Session, user_id: int, symptom_input: str, predicted_output: str):
    r = MLResult(user_id=user_id, symptom_input=symptom_input, predicted_output=predicted_output)
    db.add(r); db.commit(); db.refresh(r)
    return r
