import logging

from contextlib import asynccontextmanager
from app.core.database import Model, engine
from fastapi import FastAPI


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

        logger.info('База данных готова к работе')

        yield

        logger.info('Выключение сервера')