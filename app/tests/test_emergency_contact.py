import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_emergency_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/emergency_contacts/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": "Jane Doe",
            "phone": "+1234567890",
            "relationship": "Spouse",
        })
    assert response.status_code in [200, 201]

