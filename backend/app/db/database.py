from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from app.db.base_class import Base
from dotenv import load_dotenv
load_dotenv()

# Use async SQLite driver
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./audit.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://avaxdb_user:c6VwIOfR4yxsRUXoWg7UAEuR1mkAJ3JO@dpg-d0or2lbe5dus73d5tgo0-a.oregon-postgres.render.com/avaxdb'
# SQLALCHEMY_DATABASE_URL = 'postgresql://neondb_owner:npg_XjcEVRkxdw35@ep-red-hat-a84p9nf1-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal = sessionmaker( 
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session