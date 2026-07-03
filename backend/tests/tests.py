import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

from backend.database import test_session, test_engine
from backend.main import app, get_db
from backend.models import Base

# Provies database session for testing, overrides get_db dependancy in the 
# FastAPI app to use the test database instead of the production database
async def override_get_db():
    async with test_session() as session:
        yield session

# Replace get_db with override_get_db for all tests
app.dependency_overrides[get_db] = override_get_db

# Runs before and after each test
@pytest_asyncio.fixture(autouse=True) # autouse means every test gets fresh empty tables
async def setup_db():
    # Create tables before each test, drop them after
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# HTTP client fixture
@pytest_asyncio.fixture
# Creates AsyncClient for making HTTP requests to FastAPI during tests
# Uses ASGITransport to interact with app without starting server
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# Testing GET root 
@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe Box API"}