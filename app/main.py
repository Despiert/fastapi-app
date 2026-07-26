import logging

from fastapi import FastAPI

from app.api import user_router, item_router, stat_router
from app.core.lifespan import lifespan
from app.utils.handlers import register_exception_handlers, server_error_handlers


logging.basicConfig(level=logging.INFO)

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
server_error_handlers(app)

app.include_router(user_router)
app.include_router(item_router)
app.include_router(stat_router)