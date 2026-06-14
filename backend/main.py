from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Recipe Box API"}

recipes = [
    {
        "id": 1,
        "name": "Chicken Nuggets"
    }
]

@app.get("/recipes/{recipe_id}")
def get_recipes(recipe_id: int) -> str:
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return recipe["name"]
        else:
            raise HTTPException(status_code=404, detail=f"Recipe not found")