from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select
from datetime import datetime
from app.database import get_db
from app.models import Event


async def update_event_status():
    # Update event statuses to 'completed' if their end_time has passed
    async for db in get_db():
        try:
            current_time = datetime.now()
            result = await db.execute(
                select(Event).filter(Event.status != "completed")
            )
            events = result.scalars().all()
            for event in events:
                if event.end_time < current_time:
                    event.status = "completed"
            await db.commit()
        except Exception as err:
            print(f"Error updating event statuses: {err}")


def start_scheduler():
    # Start the scheduler with AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_event_status, "interval", minutes=1)
    scheduler.start()
    print("Scheduler started!")
    return scheduler

