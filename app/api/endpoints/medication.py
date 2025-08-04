router = APIRouter()

@router.get("/", response_model=List[str])
def read_medications(db: Session = Depends(get_db)):
    return ["Sample medication"]

@router.post("/", response_model=str)
def create_medication(db: Session = Depends(get_db)):
    return "Created medication"
