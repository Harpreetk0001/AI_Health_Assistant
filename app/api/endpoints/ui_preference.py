router = APIRouter()

@router.get("/", response_model=List[str])
def read_ui_preferences(db: Session = Depends(get_db)):
    return ["Sample UI preference"]

@router.post("/", response_model=str)
def create_ui_preference(db: Session = Depends(get_db)):
    return "Created UI preference"
