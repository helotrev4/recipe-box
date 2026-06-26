from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:123Awesome@localhost:5433/recipebox"

# create database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Use AsyncSession for async operations
    autoflush=False,
    autocommit=False
)