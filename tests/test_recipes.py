import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test the root endpoint returns the expected message"""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the simplified Cookbook API!"}


@pytest.mark.asyncio
async def test_create_recipe(client, db_session):
    """Test creating a new recipe"""
    recipe_data = {
        "title": "Test Recipe",
        "cooking_time": 30,
        "description": "Test description",
        "ingredients": ["Ingredient 1", "Ingredient 2"]
    }

    response = await client.post("/recipes", json=recipe_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert data["cooking_time"] == recipe_data["cooking_time"]
    assert data["description"] == recipe_data["description"]
    assert set(data["ingredients"]) == set(recipe_data["ingredients"])
    assert data["views"] == 0
    assert "id" in data


@pytest.mark.asyncio
async def test_get_recipes(client, db_session):
    """Test retrieving all recipes"""
    # First create a recipe
    recipe_data = {
        "title": "Test Recipe",
        "cooking_time": 30,
        "description": "Test description",
        "ingredients": ["Ingredient 1", "Ingredient 2"]
    }
    await client.post("/recipes", json=recipe_data)

    # Now get all recipes
    response = await client.get("/recipes")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == recipe_data["title"]


@pytest.mark.asyncio
async def test_get_recipe_detail(client, db_session):
    """Test retrieving a specific recipe increases view count"""
    # First create a recipe
    recipe_data = {
        "title": "Test Recipe",
        "cooking_time": 30,
        "description": "Test description",
        "ingredients": ["Ingredient 1", "Ingredient 2"]
    }
    create_response = await client.post("/recipes", json=recipe_data)
    recipe_id = create_response.json()["id"]

    # Get the recipe first time
    response1 = await client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["views"] == 1

    # Get the recipe second time (view count should increase)
    response2 = await client.get(f"/recipes/{recipe_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["views"] == 2


@pytest.mark.asyncio
async def test_get_nonexistent_recipe(client, db_session):
    """Test retrieving a non-existent recipe returns 404"""
    response = await client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"