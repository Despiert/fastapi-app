from abc import ABC, abstractmethod
from sqlalchemy import select

from app.models.users import User
from app.schemas.user import UserGet
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(ABC):
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        pass

    async def get_user(self, user_id: int, session: AsyncSession):
        pass



class SQLUserRepository(UserRepository):
    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        stmt = await session.execute(select(User))
        users = stmt.scalars().all()
        return [UserGet.model_validate(user) for user in users]

    async def get_user(self, user_id: int, session: AsyncSession):
        stmt = select(User).where(User.id == user_id)
        user = await session.execute(stmt)
        result = user.scalar_one_or_none()
        if result is None:
            return None
        return UserGet.model_validate(result)

