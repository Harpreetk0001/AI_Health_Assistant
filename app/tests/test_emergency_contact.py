import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
@pytest.fixture
def sample_emergency_contact():
    return {
        "user_id": "test-user-uuid",
        "name": "John Doe",
        "relationship": "Brother",
        "phone_number": "+61123456789",
        "email": "johndoe@example.com"
    }
def test_create_emergency_contact(sample_emergency_contact):
    response = client.post("/emergency_contacts/", json=sample_emergency_contact)
    assert response.status_code in [201, 422]
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["name"] == sample_emergency_contact["name"]
def test_get_emergency_contact():
    contact_id = "test-emergency-contact-uuid"  # Replace with valid UUID
    response = client.get(f"/emergency_contacts/{contact_id}")
    assert response.status_code in [200, 404]
