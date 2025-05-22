from typing import List

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Recipe(Base):
    """Recipe model representing a cooking recipe"""
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    description: Mapped[str] = mapped_column(Text, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)

    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    ingredients = association_proxy("recipe_ingredients", "ingredient_name")


class RecipeIngredient(Base):
    """Association model for recipe ingredients"""
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_name: Mapped[str] = mapped_column(String, nullable=False)

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="recipe_ingredients")
