router = APIRouter()

@router.get("/", response_model=List[str])
def read_emergency_contacts(db: Session = Depends(get_db)):
    return ["Sample emergency contact"]

@router.post("/", response_model=str)
def create_emergency_contact(db: Session = Depends(get_db)):
    return "Created emergency contact"
