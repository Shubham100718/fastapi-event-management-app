from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLAlchemy base model
Base = declarative_base()

# Database engine
async_engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)

# Create a session
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

