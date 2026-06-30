from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

# Testing root endpoint
def test_root():

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Recipe Box API"
    }
    
# Test listing all recipes (GET /recipes)
def test_listing_recipes(): 
    
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list) # Ensure response is list

    # Every recipe should contain these keys
    if response.json():
        recipe = response.json()[0]

        assert "id" in recipe
        assert "name" in recipe
        assert "calories" in recipe
        
# Test getting specific recipe by ID and creating recipe (GET /recipes/{recipe_id})
def test_get_recipe(): # doesn't work 

    # Step 1
    create = client.post("/recipes",
        json={
            "name": "Test Recipe",
            "calories": 123
        }
    )

    recipe = create.json()

    recipe_id = recipe["id"] 

    # Step 2
    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200

    recipe = response.json()

    assert recipe["id"] == recipe_id
    assert recipe["name"] == "Test Recipe"
    assert recipe["calories"] == 123

    # Step 3
    client.delete(f"/recipes/{recipe_id}")
    
# Recipe doesn't exist
def test_get_recipe_not_found():

    response = client.get("/recipes/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"
    
# # Test deleting a recipe (DELETE)
# def test_delete_recipe():

#     recipe = {
#         "name": "Delete Me",
#         "calories": 50
#     }

#     create = client.post(
#         "/recipes",
#         json=recipe
#     )

#     recipe_id = create.json()["id"]

#     delete = client.delete(f"/recipes/{recipe_id}")

#     assert delete.status_code == 200

#     assert delete.json() == {
#         "message": f"Recipe with id {recipe_id} deleted successfully"
#     }