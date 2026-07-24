from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


class ErrorHandler:
    @staticmethod
    def raise_not_found(entity: str, identifier: str | int):
        logger.warning(f'{entity} "{identifier}" не найден')
        raise HTTPException(status_code=404, detail=f'{entity} "{identifier}" не найден')

    @staticmethod
    def raise_already_exists(entity: str, name: str | None = None):
        if name is None:
            detail = f'{entity} уже внесен в базу данных'
        else:
            detail = f'{entity} "{name}" уже внесен в базу данных'
        logger.warning(detail)
        raise HTTPException(status_code=409, detail=detail)

