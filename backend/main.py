from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import engine
from models import Base

# from typing import Optional
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Recipe Box API"}

class Recipe(BaseModel):
    id: int
    name:str # means that this is a required for creating item
    calories:int = 0
    
# recipes = [
#     # {
#     #     "id": 1,
#     #     "name": "Chicken Nuggets"
#     # },
#     # {
#     #     "id": 2,
#     #     "name": "Hamburger"
#     # }
# ]

@app.get("/recipes", response_model=list[Recipe])
def list_recipes(limit: int = 10):
    return recipes[0:limit]

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipes(recipe_id: int) -> Recipe:
    for recipe in recipes: #iterates through all the recipes
        if recipe["id"] == recipe_id:
            return Recipe(**recipe) # **recipe unpacks dict and passes keys and values to Recipe model
        
    # Raise exception only after checking all recipes
    raise HTTPException(status_code=404, detail=f"Recipe not found")

# next_id = 1 # Global variable so delete doesn't conflict ID creation in the future (placeholder until database implement)

@app.post("/recipes")
def create_recipe(recipe: Recipe): # Using BaseModel to create 
    global next_id
    new_recipe = {
        "id": next_id,
        "name": recipe.name,
        "calories": recipe.calories
    }
    next_id += 1
    recipes.append(new_recipe)
    return new_recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            recipes.remove(recipe)
            
            return {
                "message": f"Recipe {recipe_id}: {recipe["name"]} deleted successfully"
            }
            
    raise HTTPException(status_code=404, detail=f"Recipe not found")