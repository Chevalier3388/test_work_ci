from fastapi import FastAPI



from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router as recipes_routers




@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База создана")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(recipes_routers)

