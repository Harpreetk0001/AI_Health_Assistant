import pytest
from httpx import AsyncClient
from app.main import app
@pytest.mark.asyncio
async def test_create_suggestion():
    async with AsyncClient(app=app, base_url="http://MedBuddy") as ac:
        response = await ac.post("/suggestions/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "suggestion_text": "Try a 10-minute walk today.",
            "timestamp": "2025-08-04T00:00:00Z",
        })
    assert response.status_code in [200, 201]
