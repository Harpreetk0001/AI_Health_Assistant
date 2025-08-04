router = APIRouter()

@router.get("/", response_model=List[str])
def read_activity_logs(db: Session = Depends(get_db)):
    return ["Sample activity log entry"]

@router.post("/", response_model=str)
def create_activity_log(db: Session = Depends(get_db)):
    return "Created activity log entry"
