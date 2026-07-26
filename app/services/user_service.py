import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import ENTITY_USER, ENTITY_USERS
from app.repository.user_repository import UserRepository
from app.schemas.user import UserGet, UserAdd, UserPatch
from app.utils.exceptions import ErrorHandler
from app.utils.hashing import hash_password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def _get_user_or_404(self, user_id: int, session: AsyncSession):
        logger.info(f'Поиск {ENTITY_USER} с id: {user_id}')
        result = await self.repository.get_user(user_id, session)
        if result is None:
            logger.warning(f'{ENTITY_USER} с id: {user_id} не  найден')
            raise ErrorHandler.raise_not_found(ENTITY_USER, user_id)
        return result

    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        logger.info(f'Поиск {ENTITY_USERS}')
        return await self.repository.get_all(session)

    async def get_user(self, user_id: int, session: AsyncSession) -> UserGet:
        user =  await self._get_user_or_404(user_id, session)
        return UserGet.model_validate(user)

    async def del_user(self, user_id: int, session: AsyncSession):
        logger.info(f'Поиск {ENTITY_USER}')
        result = await self.repository.del_user(user_id, session)
        if result is None:
            logger.warning(f'{ENTITY_USER} с id: {user_id} не  найден')
            raise ErrorHandler.raise_not_found(ENTITY_USER, user_id)
        logger.info(f'{ENTITY_USER} с id: "{user_id}" удален(внесен в архив)')
        return {'message': 'Пользователь удален', 'user_id': user_id}

    async def add_user(self, user: UserAdd, session: AsyncSession):
        logger.info('Проверка email')
        result = await self.repository.find_by_email(user.email, session)
        if result is not None:
            logger.warning(f'{user.email} уже используется')
            raise ErrorHandler.raise_already_exists(ENTITY_USER, user.email)
        existing = await self.repository.add_user(user, session)
        logger.info('Регистрация пользователя завершена')
        return existing

    async def get_user_by_email(self, email: str, session: AsyncSession) -> UserGet:
        logger.info('Поиск по email')
        result = await self.repository.find_by_email(email, session)
        if result is None:
            logger.warning(f'{ENTITY_USER} с email {email} не найдет')
            raise ErrorHandler.raise_not_found(ENTITY_USER, email)
        return result

    async def patch_user(self, user_id: int, user: UserPatch, session: AsyncSession):
        result = await self._get_user_or_404(user_id, session)
        for key, value in user.model_dump(exclude_unset=True).items():
            if key == 'password':
                value = hash_password(value)
            setattr(result, key, value)
        return await self.repository.refresh_user(result, session)