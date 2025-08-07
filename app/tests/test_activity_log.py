import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime

from app.main import app  # adjust if your main app is elsewhere
from app.db.session import get_db
from app.db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test DB setup (in-memory or test Postgres)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for simplicity
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply override
app.dependency_overrides[get_db] = override_get_db

# Setup test client
client = TestClient(app)

# Create tables before tests
@pytest.fixture(scope="module", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Dummy UUID for user_id (replace with real one if FK constraints matter)
TEST_USER_ID = uuid4()

def test_create_activity_log():
    response = client.post("/activity_logs/", json={
        "user_id": str(TEST_USER_ID),
        "activity_type": "Walking",
        "duration_minutes": 30,
        "steps_count": 4000,
        "calories_burned": 100,
        "logged_at": datetime.now().isoformat()
    })
    assert response.status_code == 200
    data = response.json()
    assert data["activity_type"] == "Walking"
    assert "id" in data
    global created_id
    created_id = data["id"]  # Save for future tests

def test_read_all_activity_logs():
    response = client.get("/activity_logs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_activity_log_by_id():
    response = client.get(f"/activity_logs/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id

def test_update_activity_log():
    response = client.put(f"/activity_logs/{created_id}", json={
        "activity_type": "Running",
        "duration_minutes": 45
    })
    assert response.status_code == 200
    data = response.json()
    assert data["activity_type"] == "Running"
    assert data["duration_minutes"] == 45

def test_delete_activity_log():
    response = client.delete(f"/activity_logs/{created_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_read_nonexistent_activity_log():
    response = client.get(f"/activity_logs/{created_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_update_nonexistent_activity_log():
    response = client.put(f"/activity_logs/{uuid4()}", json={
        "activity_type": "Swimming"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_delete_nonexistent_activity_log():
    response = client.delete(f"/activity_logs/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
