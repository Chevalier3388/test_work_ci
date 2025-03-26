from typing import Optional

from pydantic import BaseModel, ConfigDict

class SRecipe(BaseModel):
    """
    Базовый класс
    """
    title: str
    cooking_time: int
    ingredients: Optional[str] = None  # вариант 1
    description: str | None = None  # вариант 2


# Схема для добавления рецепта
class SRecipeAdd(SRecipe):
    """
    Для добавления рецепта
    """
    pass


# Схема для детального рецепта
class SRecipeResponse(SRecipe):
    """
    Для детальной информации о рецепте.
    """
    pass

class SRecipeBadResponse(BaseModel):
    """
    Для отсутствующего рецепта.
    """
    msg: str


# Схема для списка рецептов
class SRecipeListResponse(BaseModel):
    """
    Для списка рецептов в таблице.
    """
    title: str
    cooking_time: int
    views: int

    class Config(ConfigDict):
        from_attributes = True


class SRecipeCreateResponse(BaseModel):
    """
    Для ответа на добавление рецепта
    """
    msg: str
    recipe_title: str
    recipe_id: int
