import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_event(async_client: AsyncClient, init_db):
    response = await async_client.post("/api/events", json={
        "name": "Test Event",
        "description": "Test Description",
        "start_time": "2025-01-15T10:00:00",
        "end_time": "2025-01-15T12:00:00",
        "location": "Test Location",
        "max_attendees": 100
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"


@pytest.mark.asyncio
async def test_update_event(async_client: AsyncClient, init_db):
    response = await async_client.post("/api/events", json={
        "name": "Update Event",
        "description": "Update Description",
        "start_time": "2025-01-20T10:00:00",
        "end_time": "2025-01-20T12:00:00",
        "location": "Update Location",
        "max_attendees": 100
    })
    event_id = response.json()["event_id"]
    update_response = await async_client.put(f"/api/events/{event_id}", json={
        "name": "Updated Event Name",
        "status": "ongoing"
    })
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Event Name"
    assert update_response.json()["status"] == "ongoing"


@pytest.mark.asyncio
async def test_list_events(async_client: AsyncClient, init_db):
    await async_client.post("/api/events", json={
        "name": "Test Event",
        "description": "Test Description",
        "start_time": "2025-01-15T10:00:00",
        "end_time": "2025-01-15T12:00:00",
        "location": "Test Location",
        "max_attendees": 100
    })
    response = await async_client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()) > 0

