from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Recipe Box API"}

class Recipe(BaseModel):
    id: Optional[int] = None
    name:str 
    calories:int = 0
    
recipes = [
    # {
    #     "id": 1,
    #     "name": "Chicken Nuggets"
    # },
    # {
    #     "id": 2,
    #     "name": "Hamburger"
    # }
]

@app.get("/recipes")
def list_recipes(limit: int = 10):
    return recipes[0:limit]

@app.get("/recipes/{recipe_id}")
def get_recipes(recipe_id: int) -> Recipe:
    for recipe in recipes: #iterates through all the recipes
        if recipe["id"] == recipe_id:
            return Recipe(**recipe) # **recipe unpacks dict and passes keys and values to Recipe model
        
    # Raise exception only after checking all recipes
    raise HTTPException(status_code=404, detail=f"Recipe not found")

@app.post("/recipes")
def create_recipe(recipe: Recipe): # Using BaseModel to create 
    new_recipe = {
        "id": len(recipes) + 1,
        "name": recipe.name,
        "calories": recipe.calories
    }
    
    recipes.append(new_recipe)
    return new_recipe