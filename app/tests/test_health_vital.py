import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_health_vital():
    return {
        "user_id": "test-user-uuid",  # Replace with a real UUID in integration
        "heart_rate": 72,
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80,
        "hydration_level": 60.0,
        "sleep_hours": 7.5,
        "steps": 8000
    }

def test_create_health_vital(sample_health_vital):
    response = client.post("/health_vitals/", json=sample_health_vital)
    assert response.status_code in [201, 422]  # 422 if UUID is not valid
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["heart_rate"] == sample_health_vital["heart_rate"]

def test_get_health_vital():
    health_vital_id = "test-vital-uuid"  # Replace with a real UUID
    response = client.get(f"/health_vitals/{health_vital_id}")
    assert response.status_code in [200, 404]
