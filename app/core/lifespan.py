from contextlib import asynccontextmanager
from app.core.database import Model, engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

        print('База данных готова к работе')

        yield

        print('Выключение сервера')