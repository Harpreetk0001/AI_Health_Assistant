import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "hashed_password": "securehash",
            "role": "elderly",
            "language_preference": "en",
        })
    assert response.status_code in [200, 201]

