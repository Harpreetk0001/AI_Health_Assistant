router = APIRouter()

@router.get("/", response_model=List[str])
def read_users(db: Session = Depends(get_db)):
    return ["Sample user"]

@router.post("/", response_model=str)
def create_user(db: Session = Depends(get_db)):
    return "Created user"
