from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Recipe, RecipeIngredient
from src.schemas import RecipeCreate, RecipeDetail, RecipeList

router = APIRouter(tags=["recipes"])


@router.get("/recipes", response_model=List[RecipeList])
async def get_recipes(db: AsyncSession = Depends(get_db)) -> List[RecipeList]:
    """
    Get all recipes sorted by:
    1. Number of views (descending)
    2. Cooking time (ascending)
    """
    query = select(Recipe).order_by(desc(Recipe.views), asc(Recipe.cooking_time))
    result = await db.execute(query)
    recipes: List[Recipe] = list(result.scalars().all())
    return [RecipeList.model_validate(recipe) for recipe in recipes]


@router.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)) -> RecipeDetail:
    """
    Get detailed information about a specific recipe.
    Each request increments the recipe's view counter.
    """
    query = select(Recipe).where(Recipe.id == recipe_id)
    result = await db.execute(query)
    recipe = result.scalars().first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    recipe.views = (recipe.views or 0) + 1

    await db.commit()
    await db.refresh(recipe)

    ingredients_query = select(RecipeIngredient.ingredient_name).where(RecipeIngredient.recipe_id == recipe_id)
    ingredients_result = await db.execute(ingredients_query)
    ingredients: List[str] = list(ingredients_result.scalars().all())

    recipe_id_int: int = int(recipe.id)
    title_str: str = str(recipe.title)
    cooking_time_int: int = int(recipe.cooking_time)
    description_str: str = str(recipe.description)
    views_int: int = int(recipe.views)

    return RecipeDetail(
        id=recipe_id_int,
        title=title_str,
        cooking_time=cooking_time_int,
        description=description_str,
        views=views_int,
        ingredients=ingredients
    )


@router.post("/recipes", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe_data: RecipeCreate, db: AsyncSession = Depends(get_db)) -> RecipeDetail:
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

    ingredients: List[str] = []

    query = select(RecipeIngredient.ingredient_name).where(RecipeIngredient.recipe_id == db_recipe.id)
    result = await db.execute(query)
    ingredients = list(result.scalars().all())

    recipe_id_int: int = int(db_recipe.id)
    title_str: str = str(db_recipe.title)
    cooking_time_int: int = int(db_recipe.cooking_time)
    description_str: str = str(db_recipe.description)
    views_int: int = int(db_recipe.views)

    return RecipeDetail(
        id=recipe_id_int,
        title=title_str,
        cooking_time=cooking_time_int,
        description=description_str,
        views=views_int,
        ingredients=ingredients
    )
