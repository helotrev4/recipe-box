import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.main import app, get_db
from backend.models import Base


# Separate in-memory test database, recreated for every test
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Creates async database engine for test database
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

session_test = sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False)

# Provies database session for testing, overrides get_db dependancy in the 
# FastAPI app to use the test database instead of the production database
async def override_get_db():
    async with session_test() as session:
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
# @pytest_asyncio.fixture <- not needed because of pytest.ini
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe Box API"}
        
# Testing GET /recipes

async def test_list_recipes_empty(client):
    response = await client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []

# Testing POST recipe

async def test_create_recipe(client):
    response = await client.post("/recipes", json={"name": "Pancakes", "calories": 350})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pancakes"
    assert data["calories"] == 350
    assert "id" in data
    
# Test POST recipe with no given calories

async def test_create_recipe_default_calories(client):
    # calories has a default of 0, should work without it
    response = await client.post("/recipes", json={"name": "Toast"})
    assert response.status_code == 200
    assert response.json()["calories"] == 0
    
# Test find recipe not found

async def test_get_recipe_not_found(client):
    response = await client.get("/recipes/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"
    
# Test UPDATE recipe

async def test_update_recipe(client):
    create_resp = await client.post("/recipes", json={"name": "Salad", "calories": 100})
    recipe_id = create_resp.json()["id"]

    response = await client.put(f"/recipes/{recipe_id}", json={"name": "Big Salad", "calories": 250})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Big Salad"
    assert data["calories"] == 250
    
# Test update recipe not found

async def test_update_recipe_not_found(client):
    response = await client.put("/recipes/9999", json={"name": "Ghost", "calories": 0})
    assert response.status_code == 404
    
# Test DELETE recipe

async def test_delete_recipe(client):
    create_resp = await client.post("/recipes", json={"name": "Soup", "calories": 150})
    recipe_id = create_resp.json()["id"]

    response = await client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

    # Confirm it's actually gone
    get_resp = await client.get(f"/recipes/{recipe_id}")
    assert get_resp.status_code == 404

# Test delete recipe not found

async def test_delete_recipe_not_found(client):
    response = await client.delete("/recipes/9999")
    assert response.status_code == 404

# Test GET /recipes correct listing

async def test_list_recipes_after_create(client):
    await client.post("/recipes", json={"name": "A", "calories": 10})
    await client.post("/recipes", json={"name": "B", "calories": 20})

    response = await client.get("/recipes")
    assert response.status_code == 200
    names = [r["name"] for r in response.json()]
    # extracts name from each recipe in the response
    
    assert names == ["A", "B"]  # ordered by id, matches your `.order_by(RecipeModel.id)`
