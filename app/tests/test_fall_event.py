import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
@pytest.fixture
def sample_fall_event():
    return {
        "user_id": "test-user-uuid",  # Replace with a valid UUID for integration test
        "fall_detected": True,
        "fall_time": "2025-08-05T14:30:00Z",
        "location": "Bathroom"
    }
def test_create_fall_event(sample_fall_event):
    response = client.post("/fall_events/", json=sample_fall_event)
    assert response.status_code in [201, 422]
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["fall_detected"] == sample_fall_event["fall_detected"]
def test_get_fall_event():
    fall_event_id = "test-fall-event-uuid"  # Replace with real UUID
    response = client.get(f"/fall_events/{fall_event_id}")
    assert response.status_code in [200, 404]
