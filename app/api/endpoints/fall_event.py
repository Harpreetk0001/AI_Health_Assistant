router = APIRouter()

@router.get("/", response_model=List[str])
def read_fall_events(db: Session = Depends(get_db)):
    return ["Sample fall event"]

@router.post("/", response_model=str)
def create_fall_event(db: Session = Depends(get_db)):
    return "Created fall event"
