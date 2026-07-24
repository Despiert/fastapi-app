import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import ENTITY_USER, ENTITY_USERS
from app.repository.user_repository import UserRepository
from app.schemas.user import UserGet

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        logger.info(f'Поиск {ENTITY_USERS}')
        return await self.repository.get_all(session)
