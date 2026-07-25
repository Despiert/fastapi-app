import bcrypt
from fastapi import APIRouter
from fastapi import HTTPException, status
from sqlalchemy import select

from app.repository.user_repository import SQLUserRepository
from app.schemas.user import UserAdd, UserGet, UserDel, UserPatch
from app.core.database import SessionDep
from app.models.users import User, UserArchive
from app.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])

repo = SQLUserRepository()
service = UserService(repository=repo)

@user_router.get('/all', response_model=list[UserGet], status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep):
    return await service.get_all(session)

@user_router.post('/user', status_code=status.HTTP_201_CREATED)
async def add_user(user: UserAdd, session: SessionDep):
    stmt = select(User).where(User.email == user.email, User.is_active == True)
    result = await session.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail='email уже зарегистрирован')

    new_user = User(**user.model_dump())
    new_user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    session.add(new_user)
    await session.commit()
    return 'Регистрация завершена'

@user_router.get('/{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: SessionDep):
    return await service.get_user(user_id, session)


@user_router.delete('/{user_id}',response_model=UserDel, status_code=status.HTTP_200_OK)
async def user_del(user_id: int, session: SessionDep):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        user.is_active = False
        user_archive = UserArchive(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=False,
            registered_at=user.registered_at
        )

        session.add(user_archive)
        await session.delete(user)
        await session.commit()
        return {'message': 'Пользователь удален', 'user_id': user_id}
    raise HTTPException(status_code=404, detail="User not found")

@user_router.patch('/{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def user_patch(user_id: int, user: UserPatch, session: SessionDep):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user_res = result.scalar_one_or_none()
    if user_res is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        if key == 'password':
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        setattr(user_res, key, value)
    session.add(user_res)
    await session.commit()
    await session.refresh(user_res)
    return user_res

@user_router.put('//{user_id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def user_up(user_id: int, user: UserAdd, session: SessionDep):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user_upd = result.scalar_one_or_none()
    if user_upd is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump().items():
        if key == 'password':
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        setattr(user_upd, key, value)
    session.add(user_upd)
    await session.commit()
    await session.refresh(user_upd)
    return user_upd