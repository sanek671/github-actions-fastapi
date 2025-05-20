from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Recipe, RecipeIngredient
from schemas import RecipeList, RecipeDetail, RecipeCreate

router = APIRouter(tags=["recipes"])


@router.get("/recipes", response_model=List[RecipeList])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    """
    Get all recipes sorted by:
    1. Number of views (descending)
    2. Cooking time (ascending)
    """
    query = select(Recipe).order_by(desc(Recipe.views), asc(Recipe.cooking_time))
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get detailed information about a specific recipe.
    Each request increments the recipe's view counter.
    """
    query = select(Recipe).where(Recipe.id == recipe_id)
    result = await db.execute(query)
    recipe = result.scalars().first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)

    ingredients_query = select(RecipeIngredient.ingredient_name).where(RecipeIngredient.recipe_id == recipe_id)
    ingredients_result = await db.execute(ingredients_query)
    ingredients = ingredients_result.scalars().all()

    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "cooking_time": recipe.cooking_time,
        "description": recipe.description,
        "views": recipe.views,
        "ingredients": ingredients
    }

    return recipe_dict


@router.post("/recipes", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe_data: RecipeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new recipe"""
    db_recipe = Recipe(
        title=recipe_data.title,
        cooking_time=recipe_data.cooking_time,
        description=recipe_data.description,
    )
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)

    for ingredient in recipe_data.ingredients:
        db_ingredient = RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_name=ingredient
        )
        db.add(db_ingredient)

    await db.commit()
    await db.refresh(db_recipe)

    ingredients = []
    query = select(RecipeIngredient.ingredient_name).where(RecipeIngredient.recipe_id == db_recipe.id)
    result = await db.execute(query)
    ingredients = result.scalars().all()

    recipe_dict = {
        "id": db_recipe.id,
        "title": db_recipe.title,
        "cooking_time": db_recipe.cooking_time,
        "description": db_recipe.description,
        "views": db_recipe.views,
        "ingredients": ingredients
    }

    return recipe_dict