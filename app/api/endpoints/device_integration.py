router = APIRouter()

@router.get("/", response_model=List[str])
def read_device_integrations(db: Session = Depends(get_db)):
    return ["Sample device integration"]

@router.post("/", response_model=str)
def create_device_integration(db: Session = Depends(get_db)):
    return "Created device integration"
