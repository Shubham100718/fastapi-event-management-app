from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from .database import Base, async_engine
from .routes.auth_routes import auth_router
from .routes.events_routes import event_router
from .routes.attendees_routes import attendee_router
from .scheduler.scheduler import start_scheduler


# Create database tables asynchronously
async def create_tables():
    """Create all database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    await create_tables()
    start_scheduler()
    yield
    # Code to run on shutdown (if needed)
    pass

app = FastAPI(lifespan=lifespan)

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

