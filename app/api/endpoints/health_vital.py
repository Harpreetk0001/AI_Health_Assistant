router = APIRouter()

@router.get("/", response_model=List[str])
def read_health_vitals(db: Session = Depends(get_db)):
    return ["Sample health vital"]

@router.post("/", response_model=str)
def create_health_vital(db: Session = Depends(get_db)):
    return "Created health vital"
