import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_attendee(async_client: AsyncClient, init_db):
    event_response = await async_client.post("/api/events", json={
        "name": "Attendee Event",
        "description": "Event for attendees",
        "start_time": "2025-01-15T10:00:00",
        "end_time": "2025-01-15T12:00:00",
        "location": "Test Location",
        "max_attendees": 2
    })
    event_id = event_response.json().get("event_id")
    attendee_response = await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890"
    })
    assert attendee_response.status_code == 200
    assert attendee_response.json()["first_name"] == "John"


@pytest.mark.asyncio
async def test_register_attendee_limit(async_client: AsyncClient, init_db):
    event_response = await async_client.post("/api/events", json={
        "name": "Attendee Event",
        "description": "Event for attendees",
        "start_time": "2025-01-15T10:00:00",
        "end_time": "2025-01-15T12:00:00",
        "location": "Test Location",
        "max_attendees": 2
    })
    event_id = event_response.json().get("event_id")
    await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "1234567891"
    })
    await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Max",
        "last_name": "Doe",
        "email": "max.doe@example.com",
        "phone_number": "1234567891"
    })
    response = await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Max",
        "last_name": "Smith",
        "email": "max.smith@example.com",
        "phone_number": "1234567892"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Max attendees limit reached"


@pytest.mark.asyncio
async def test_check_in_attendees(async_client: AsyncClient, init_db):
    event_response = await async_client.post("/api/events", json={
        "name": "Attendee Event",
        "description": "Event for attendees",
        "start_time": "2025-01-26T10:00:00",
        "end_time": "2025-01-26T12:00:00",
        "location": "Test Location",
        "max_attendees": 100
    })
    event_id = event_response.json().get("event_id")
    attendee_creation_response = await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "1234567891"
    })
    assert attendee_creation_response.status_code == 200  # or the appropriate status code

    attendee_response = await async_client.get(f"/api/attendees/{event_id}")

    attendees = attendee_response.json()
    assert len(attendees) > 0, "No attendees found for the event."
    attendee_id = attendees[0]["attendee_id"]

    check_in_response = await async_client.put("/api/attendees/check-in", json={
        "attendee_ids": [attendee_id]
    })
    assert check_in_response.status_code == 200
    assert check_in_response.json()["message"] == "Attendees checked in successfully"


@pytest.mark.asyncio
async def test_bulk_check_in(async_client: AsyncClient, init_db):
    # Create an event
    event_response = await async_client.post("/api/events", json={
        "name": "Attendee Event",
        "description": "Event for attendees",
        "start_time": "2025-01-15T10:00:00",
        "end_time": "2025-01-15T12:00:00",
        "location": "Test Location",
        "max_attendees": 100
    })
    event_id = event_response.json().get("event_id")
    # Add attendees
    await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "1234567891"
    })
    await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Jane1",
        "last_name": "Doe",
        "email": "jane1.doe@example.com",
        "phone_number": "1234567891"
    })
    await async_client.post(f"/api/attendees/{event_id}", json={
        "first_name": "Jane2",
        "last_name": "Doe",
        "email": "jane2.doe@example.com",
        "phone_number": "1234567891"
    })
    csv_content = "1\n2\n3"
    response = await async_client.post(f"/api/attendees/check-in/csv/{event_id}", files={
        "file": ("attendees.csv", csv_content, "text/csv")
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Bulk check-in successful"

