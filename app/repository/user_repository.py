from abc import ABC, abstractmethod
from sqlalchemy import select

from app.models.users import User, UserArchive
from app.schemas.user import UserGet, UserArchiveAdd, UserAdd
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(ABC):
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[UserGet]:
        pass

    @abstractmethod
    async def get_user(self, user_id: int, session: AsyncSession):
        pass

    @abstractmethod
    async def del_user(self, user_id: int, session: AsyncSession):
        pass

    @abstractmethod
    async def add_user(self, user: UserAdd, session: AsyncSession):
        pass

    @abstractmethod
    async def find_by_email(self, email: str, session: AsyncSession):
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

    async def del_user(self, user_id: int, session: AsyncSession):
        user = await session.get(User, user_id)
        if user is None or user.is_active == False:
            return None
        archive_user = UserArchiveAdd.model_validate(user).model_dump()
        archive_user['is_active'] = False
        user_archive = UserArchive(**archive_user)
        session.add(user_archive)

        await session.delete(user)
        await session.commit()

        return user_archive

    async def find_by_email(self, email: str, session: AsyncSession):
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_user(self, user: UserAdd, session: AsyncSession):
        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        return UserGet.model_validate(new_user)
