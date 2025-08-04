router = APIRouter()

@router.get("/", response_model=List[str])
def read_reminder_logs(db: Session = Depends(get_db)):
    return ["Sample reminder log"]

@router.post("/", response_model=str)
def create_reminder_log(db: Session = Depends(get_db)):
    return "Created reminder log"
