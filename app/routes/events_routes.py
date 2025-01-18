from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User, Event, EventStatus
from app.schemas.events_schema import EventCreate, EventUpdate, EventResponse
from app.utils.auth_utils import get_current_user
from typing import Optional, List
from datetime import date


event_router = APIRouter()

@event_router.post("/events", response_model=EventResponse)
async def create_event(event: EventCreate, 
                    db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)
    ):
    new_event = Event(**event.dict())
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event


@event_router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, 
                    event: EventUpdate, 
                    db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)
    ):
    result = await db.execute(select(Event).filter(Event.event_id==event_id))
    db_event = result.scalar_one_or_none()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Event not found")
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@event_router.get("/events", response_model=List[EventResponse])
async def list_events(status: Optional[EventStatus] = None,
                    location: Optional[str] = None,
                    start_date: Optional[date] = None,
                    end_date: Optional[date] = None,
                    db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)
    ):
    query = select(Event)
    if status:
        query = query.filter(Event.status==status)
    if location:
        query = query.filter(Event.location==location)
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    result = await db.execute(query)
    events = result.scalars().all()
    return events

