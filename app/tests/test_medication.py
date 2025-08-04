import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_medication():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/medications/", json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": "Aspirin",
            "dosage": "100mg",
            "frequency": "daily",
            "start_date": "2025-08-04",
            "end_date": "2025-08-14",
        })
    assert response.status_code in [200, 201]

