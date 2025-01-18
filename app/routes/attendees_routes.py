from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import User, Attendee, Event
from app.schemas.attendees_schema import AttendeeCreate, AttendeeCheckIn, AttendeeResponse
from app.utils.auth_utils import get_current_user
from app.utils.csv_handler import process_csv


attendee_router = APIRouter()

@attendee_router.post("/attendees/{event_id}", response_model=AttendeeResponse)
async def register_attendee(attendee: AttendeeCreate,
                            event_id: int,
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user)
    ):
    # Check if the event exists
    event_result = await db.execute(select(Event).filter(Event.event_id==event_id))
    event = event_result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if max_attendees limit is reached
    attendee_count_result = await db.execute(
        select(Attendee).filter(Attendee.event_id==event_id)
    )
    current_attendees = attendee_count_result.scalars().all()
    if len(current_attendees) >= event.max_attendees:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Max attendees limit reached")

    # Register the attendee
    new_attendee = Attendee(**attendee.dict(), event_id=event_id)
    db.add(new_attendee)
    try:
        await db.commit()
        await db.refresh(new_attendee)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An attendee with this email is already registered."
        )
    return new_attendee


@attendee_router.get("/attendees/{event_id}", response_model=List[AttendeeResponse])
async def list_attendees(event_id: int, 
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)
    ):
    result = await db.execute(select(Attendee).filter(Attendee.event_id==event_id))
    attendees = result.scalars().all()
    if not attendees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No attendees found for the specified event")
    return attendees


@attendee_router.put("/attendees/check-in")
async def check_in_attendees(payload: AttendeeCheckIn,
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user)
    ):
    # Fetch attendees matching the provided IDs
    result = await db.execute(
        select(Attendee).filter(Attendee.attendee_id.in_(payload.attendee_ids))
    )
    attendees = result.scalars().all()
    if not attendees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendees found for the provided IDs"
        )
    # Update check-in status for each attendee
    for attendee in attendees:
        attendee.check_in_status = True
    await db.commit()
    return {
        "message": "Attendees checked in successfully",
        "checked_in_attendees": [attendee.attendee_id for attendee in attendees]
    }


@attendee_router.post("/attendees/check-in/csv/{event_id}")
async def bulk_check_in(event_id: int,
                        file: UploadFile = File(...),
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)
    ):
    # Process the uploaded CSV file
    attendee_ids = process_csv(file.file)
    # Fetch attendees matching the IDs and event
    result = await db.execute(
        select(Attendee).filter(
            Attendee.event_id == event_id, Attendee.attendee_id.in_(attendee_ids)
        )
    )
    attendees = result.scalars().all()
    if not attendees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendees found for the provided IDs"
        )
    # Update check-in status for each attendee
    for attendee in attendees:
        attendee.check_in_status = True
    await db.commit()
    return {
        "message": f"Bulk check-in successful for {len(attendees)} attendees",
        "checked_in_attendees": [attendee.attendee_id for attendee in attendees]
    }

