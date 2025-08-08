import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
@pytest.fixture
def sample_user():
    return {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "password": "StrongPass123!",
        "role": "elderly",
        "language_preference": "en"
    }
def test_create_user(sample_user):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user["email"]
    assert data["role"] == sample_user["role"]
def test_get_user():
    # Replace with actual UUID if testing live
    user_id = "test-uuid"
    response = client.get(f"/users/{user_id}")
    assert response.status_code in [200, 404]
