from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, HTTPException

from repository import RecipRepository
from schmas import (
    SRecipeAdd,
    SRecipeBadResponse,
    SRecipeCreateResponse,
    SRecipeListResponse,
    SRecipeResponse,
)

router = APIRouter(prefix="/recipes", tags=["Рецепты"])


@router.post(
    "",
    response_model=SRecipeCreateResponse,
    summary="Добавить рецепт",
    description="Добавление нового рецепта в базу данных.",
)
async def add_recipe(recipe: Annotated[SRecipeAdd, Depends()]):
    recipe_info = await RecipRepository.add_recipe(recipe)
    return {
        "msg": "Рецепт добавлен",
        "recipe_title": recipe_info[0],
        "recipe_id": recipe_info[1],
    }


@router.get(
    "",
    response_model=List[SRecipeListResponse],
    summary="Получить список рецептов",
    description="Возвращает список рецептов с полями: "
    "название, количество просмотров, время приготовления.",
)
async def get_recipes():
    recipes = await RecipRepository.get_all_recipes()
    return recipes


@router.get(
    "/{id}",
    response_model=Union[SRecipeResponse, SRecipeBadResponse],
    summary="Получить рецепт по ID",
    description="Возвращает детальную информацию по рецепту с указанным ID.",
)
async def get_recipe(id: int):
    recipe = await RecipRepository.get_recipe(id)
    if not recipe:
        raise HTTPException(
            status_code=404,
            detail=SRecipeBadResponse(msg=f"Рецепт c id {id} не найден").model_dump(),
        )
    return recipe
