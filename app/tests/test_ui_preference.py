import pytest
from httpx import AsyncClient
from app.main import app
@pytest.mark.asyncio
async def test_create_ui_preference():
    async with AsyncClient(app=app, base_url="http://MedBuddy") as ac:
        response = await ac.post("/ui_preferences/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "theme": "dark",
            "font_size": "large",
        })
    assert response.status_code in [200, 201]
