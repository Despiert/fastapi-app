import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import ENTITY_USER, ENTITY_USERS
from app.repository.user_repository import UserRepository
from app.schemas.user import UserGet
from app.utils.exceptions import ErrorHandler

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        logger.info(f'Поиск {ENTITY_USERS}')
        return await self.repository.get_all(session)

    async def get_user(self, user_id: int, session: AsyncSession) -> UserGet:
        logger.info(f'Поиск {ENTITY_USER} с id: {user_id}')
        result = await self.repository.get_user(user_id, session)
        if result is None:
            logger.warning(f'{ENTITY_USER} с id: {user_id} не  найден')
            raise ErrorHandler.raise_not_found(ENTITY_USER, user_id)
        return result

    async def del_user(self, user_id: int, session: AsyncSession):
        logger.info(f'Поиск {ENTITY_USER}')
        result = await self.repository.del_user(user_id, session)
        if result is None:
            logger.warning(f'{ENTITY_USER} с id: {user_id} не  найден')
            raise ErrorHandler.raise_not_found(ENTITY_USER, user_id)
        logger.info(f'{ENTITY_USER} с id: "{user_id}" удален(внесен в архив)')
        return {'message': 'Пользователь удален', 'user_id': user_id}