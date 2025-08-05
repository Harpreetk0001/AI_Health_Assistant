import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_activity():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/activity_logs/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "activity_type": "walking",
            "duration_minutes": 30,
            "timestamp": "2025-08-04T00:00:00Z",
        })
    assert response.status_code == 200 or response.status_code == 201

@pytest.mark.asyncio
async def test_read_activities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/activity_logs/")
    assert response.status_code == 200

