import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_fall_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/fall_events/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "detected_time": "2025-08-04T00:00:00Z",
            "severity": "moderate",
        })
    assert response.status_code in [200, 201]

