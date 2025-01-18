import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()

