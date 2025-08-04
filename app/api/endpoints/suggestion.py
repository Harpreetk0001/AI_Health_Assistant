router = APIRouter()

@router.get("/", response_model=List[str])
def read_suggestions(db: Session = Depends(get_db)):
    return ["Sample suggestion"]

@router.post("/", response_model=str)
def create_suggestion(db: Session = Depends(get_db)):
    return "Created suggestion"
