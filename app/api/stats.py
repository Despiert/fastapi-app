from fastapi import APIRouter, status
from app.core.database import SessionDep
from app.models.items import Item
from app.models.users import User
from sqlalchemy import select


stat_router = APIRouter()

@stat_router.get("/stats/items", status_code=status.HTTP_200_OK)
async def stat_items(session: SessionDep):
    stmt = select(Item)
    result = await session.execute(stmt)
    items = result.scalars().all()
    return {'Позиций':len(items)}

@stat_router.get("/stats/users", status_code=status.HTTP_200_OK)
async def stat_users(session: SessionDep):
    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return [{'number': key, 'name':user.username} for key, user in enumerate(users,1)]

@stat_router.get('/stats/stock', status_code=status.HTTP_200_OK)
async def stat_stock(session: SessionDep):
    stmt = select(Item)
    result = await session.execute(stmt)
    items = result.scalars().all()
    return {'Общее количество товара на складе':sum(item.stock_quantity for item in items)}