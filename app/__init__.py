from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .database import Base, async_engine
from .routes.auth_routes import auth_router
from .routes.events_routes import event_router
from .routes.attendees_routes import attendee_router
from .scheduler.scheduler import start_scheduler


app = FastAPI()

# Create database tables asynchronously
async def create_tables():
    """Create all database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize the app
@app.on_event("startup")
async def startup_event():
    # Create tables on startup
    await create_tables()
    # Start the scheduler
    start_scheduler()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Event Management API"}

# Include the routes
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(event_router, prefix="/api", tags=["Events"])
app.include_router(attendee_router, prefix="/api", tags=["Attendees"])
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

