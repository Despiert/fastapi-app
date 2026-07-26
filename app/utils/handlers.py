from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        logger.warning('Введены некорректные данные')
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"message": "Некорректные данные"}
        )

def server_error_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f'Неожиданная ошибка')
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )