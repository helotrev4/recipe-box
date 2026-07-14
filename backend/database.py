import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# create database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Use AsyncSession for async operations
    autoflush=False,
    autocommit=False
)

