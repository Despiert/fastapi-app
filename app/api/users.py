from fastapi import APIRouter
from fastapi import status

from app.repository.user_repository import SQLUserRepository
from app.schemas.user import UserAdd, UserGet, UserDel, UserPatch
from app.core.database import SessionDep
from app.services.user_service import UserService


user_router = APIRouter(prefix="/users", tags=["users"])

repo = SQLUserRepository()
service = UserService(repository=repo)


@user_router.get('/all', response_model=list[UserGet], status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep):
    return await service.get_all(session)


@user_router.post('/user', response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserAdd, session: SessionDep):
    return await service.add_user(user, session)


@user_router.get('/{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: SessionDep):
    return await service.get_user(user_id, session)


@user_router.delete('/{user_id}',response_model=UserDel, status_code=status.HTTP_200_OK)
async def user_del(user_id: int, session: SessionDep):
    return await service.del_user(user_id, session)


@user_router.get('/email/{email}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user_by_email(email: str, session: SessionDep):
    return await service.get_user_by_email(email, session)


@user_router.patch('/{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def user_patch(user_id: int, user: UserPatch, session: SessionDep):
    return await service.patch_user(user_id, user, session)


@user_router.put('/{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def user_up(user_id: int, user: UserAdd, session: SessionDep):
    return await service.put_user(user_id, user, session)