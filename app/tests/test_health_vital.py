import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_health_vital():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/health_vitals/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "type": "blood_pressure",
            "value": "120/80",
            "unit": "mmHg",
            "timestamp": "2025-08-04T00:00:00Z",
        })
    assert response.status_code in [200, 201]
