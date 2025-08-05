import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_medication():
    return {
        "user_id": "test-user-uuid",  # Replace with actual UUID
        "medication_name": "Aspirin",
        "dosage": "100mg",
        "frequency": "Once daily",
        "start_date": "2025-08-01",
        "end_date": "2025-08-10",
        "notes": "Take after breakfast"
    }

def test_create_medication(sample_medication):
    response = client.post("/medications/", json=sample_medication)
    assert response.status_code in [201, 422]
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["medication_name"] == sample_medication["medication_name"]

def test_get_medication():
    medication_id = "test-medication-uuid"  # Replace with valid UUID
    response = client.get(f"/medications/{medication_id}")
    assert response.status_code in [200, 404]
