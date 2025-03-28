from sqlalchemy import select

from database import RecipesOrm, new_session
from schmas import SRecipeAdd


class RecipRepository:
    @classmethod
    async def add_recipe(cls, data: SRecipeAdd):
        async with new_session() as session:
            recipe_dict = data.model_dump()

            recipe = RecipesOrm(**recipe_dict)
            session.add(recipe)
            await session.flush()
            await session.commit()
            return recipe.title, recipe.id

    @classmethod
    async def get_all_recipes(cls):
        async with new_session() as session:
            query = select(
                RecipesOrm.title, RecipesOrm.views, RecipesOrm.cooking_time
            ).order_by(RecipesOrm.views.desc(), RecipesOrm.cooking_time)

            result = await session.execute(query)

            recipes_models = [
                {"title": row[0], "views": row[1], "cooking_time": row[2]}
                for row in result.fetchall()
            ]
            return recipes_models

    @classmethod
    async def get_recipe(cls, id: int):
        async with new_session() as session:
            query = select(
                RecipesOrm.title,
                RecipesOrm.cooking_time,
                RecipesOrm.ingredients,
                RecipesOrm.description,
            ).filter(RecipesOrm.id == id)
            result = await session.execute(query)
            recipe_obj = result.fetchone()

            if not recipe_obj:
                return None

            await session.execute(
                RecipesOrm.__table__.update()
                .where(RecipesOrm.id == id)
                .values(views=RecipesOrm.views + 1)  # Увеличение views
            )
            await session.commit()

            return {
                "title": recipe_obj[0],
                "cooking_time": recipe_obj[1],
                "ingredients": recipe_obj[2],
                "description": recipe_obj[3],
            }
