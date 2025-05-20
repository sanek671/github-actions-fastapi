from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base


class Recipe(Base):
    """Recipe model representing a cooking recipe"""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    cooking_time = Column(Integer, nullable=False)  # in minutes
    description = Column(Text, nullable=False)
    views = Column(Integer, default=0)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    ingredients = association_proxy("recipe_ingredients", "ingredient_name")


class RecipeIngredient(Base):
    """Association model for recipe ingredients"""
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_name = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")