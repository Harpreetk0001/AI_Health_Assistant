import pytest
from httpx import AsyncClient
from app.main import app
@pytest.mark.asyncio
async def test_create_reminder_log():
    async with AsyncClient(app=app, base_url="http://MedBuddy") as ac:
        response = await ac.post("/reminder_logs/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "reminder_text": "Take your medication.",
            "scheduled_time": "2025-08-04T09:00:00Z",
        })
    assert response.status_code in [200, 201]
