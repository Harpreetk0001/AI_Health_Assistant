import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_device_integration():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/device_integrations/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "device_name": "SmartWatch",
            "device_type": "Wearable",
            "integration_status": "active",
        })
    assert response.status_code == 200 or response.status_code == 201

