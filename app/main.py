import logging

from fastapi import FastAPI

from app.api import user_router, item_router, stat_router
from app.core.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(item_router)
app.include_router(stat_router)

logging.basicConfig(level=logging.INFO)