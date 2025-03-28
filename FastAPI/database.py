from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///recipes.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class RecipesOrm(Model):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cooking_time: Mapped[int]
    description: Mapped[str | None]  # вариант 1
    ingredients: Mapped[Optional[str]]  # вариант 2
    views: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<Recipe(id={self.id}, title={self.title})>"


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
