from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    calories = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # stores ID of user that owns the recipe, foreign key points 
    # users.id, database enforce value must match existing user
    
    owner = relationship("User", back_populates="recipes")
    # not a database column, ORM relationship to access in code (recipe.owner)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    recipes = relationship("Recipe", back_populates="owner")
    # allow access to all recipe belonging to one user (user.recipes)

     