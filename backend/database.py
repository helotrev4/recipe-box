from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Use AsyncSession for async operations
    autoflush=False,
    autocommit=False
)

# Separate in-memory test database, recreated for every test
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Creates async database engine for test database
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

session_test = sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False)
