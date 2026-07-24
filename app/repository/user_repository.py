from abc import ABC, abstractmethod
from sqlalchemy import select

from app.models.users import User
from app.schemas.user import UserGet
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(ABC):
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        pass


class SQLUserRepository(UserRepository):
    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        stmt = await session.execute(select(User))
        users = stmt.scalars().all()
        return [UserGet.model_validate(user) for user in users]
