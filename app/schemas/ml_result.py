from pydantic import BaseModel

class MLResultIn(BaseModel):
    symptom_input: str

class MLResultOut(BaseModel):
    id: int
    predicted_output: str
    class Config:
        orm_mode = True
