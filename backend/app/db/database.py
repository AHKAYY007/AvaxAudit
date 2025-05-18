from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from app.db.base_class import Base
from dotenv import load_dotenv
load_dotenv()

# Use async SQLite driver
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./audit.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session