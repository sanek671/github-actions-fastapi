from typing import List
from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    """Base schema for recipe data"""
    title: str = Field(..., description="Recipe title")
    cooking_time: int = Field(..., description="Cooking time in minutes", gt=0)


class RecipeCreate(RecipeBase):
    """Schema for recipe creation"""
    ingredients: List[str] = Field(..., description="List of ingredients")
    description: str = Field(..., description="Recipe preparation description")


class RecipeList(RecipeBase):
    """Schema for recipe list response"""
    id: int
    views: int

    class Config:
        from_attributes = True


class RecipeDetail(RecipeBase):
    """Schema for detailed recipe response"""
    id: int
    ingredients: List[str]
    description: str
    views: int

    class Config:
        from_attributes = True