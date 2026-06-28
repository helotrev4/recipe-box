from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database import engine, async_session
from models import Base, Recipe as RecipeModel

app = FastAPI()

# Initialize the database tables

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def root():
    return {"message": "Recipe Box API"}

class RecipeBase(BaseModel):
    id: int
    name:str # means that this is a required for creating item
    calories:int = 0
    
class Config:
    orm_mode = True  # Enable ORM mode for SQLAlchemy models

class RecipeCreate(RecipeBase):
    pass  # Used for creating recipes, excludes `id`

class Recipe(RecipeBase):
    id: int  # Include `id` for responses
    
# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        yield session

db_dependancy = Depends(get_db)

@app.get("/recipes", response_model=list[Recipe]) #results in a list of objects
async def list_recipes(db: AsyncSession = db_dependancy): # async, Python does other work in the meantime
    # await -> pause until database responds
    # SELECT * FROM recipes; run in SQL 
    result = await db.execute(select(RecipeModel)) #before calling function, run get_db()
    recipes = result.scalars().all() # extracts model object, puts them in a list
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, db: AsyncSession = db_dependancy):
    result = await db.execute(select(RecipeModel).where(RecipeModel.id == recipe_id))
    recipe = result.scalar()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = db_dependancy): # sneds a JSON, converted to RecipeCreate object
    new_recipe = RecipeModel(name=recipe.name, calories=recipe.calories) # becomes RecipeModel (database row)
    db.add(new_recipe)
    await db.commit() # actually writes row to database
    # INSERT INTO recipes
    
    await db.refresh(new_recipe)  # Refresh to get the auto-generated id
    return new_recipe

@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: AsyncSession = db_dependancy):
    result = await db.execute(select(RecipeModel).where(RecipeModel.id == recipe_id))
    recipe = result.scalar()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await db.delete(recipe)
    await db.commit()
    return {"message": f"Recipe with id {recipe_id} deleted successfully"}