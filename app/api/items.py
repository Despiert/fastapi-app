from fastapi import APIRouter, status

from app.schemas.item import ItemAdd, ItemUpdate
from app.core.database import SessionDep
from app.services.item_service import ItemService


item_router = APIRouter(prefix='/items', tags=['items'])


@item_router.post('/item', response_model=ItemAdd, status_code=status.HTTP_201_CREATED)
async def item_add(item: ItemAdd, session: SessionDep):
    return await ItemService.add_new_item(item, session)


@item_router.get('/all', response_model=list[ItemAdd], status_code=status.HTTP_200_OK)
async def item_all(session: SessionDep):
    return await ItemService.get_all(session)


@item_router.get('/search', response_model=list[ItemAdd], status_code=status.HTTP_200_OK)
async def search(item_search: str, session: SessionDep):
    return await ItemService.search_items(item_search, session)


@item_router.get('/{item_id}', response_model=ItemAdd, status_code=status.HTTP_200_OK)
async def get_item(item_id: int, session: SessionDep):
    return await ItemService.get_item(item_id, session)


@item_router.delete('/{item_id}', status_code=status.HTTP_200_OK)
async def item_del(item_id: int, session: SessionDep):
    return await ItemService.del_item(item_id, session)


@item_router.patch('/{item_id}', response_model=ItemUpdate, status_code=status.HTTP_200_OK)
async def item_update(item_id: int, item: ItemUpdate, session: SessionDep):
    return await ItemService.patch_item(item_id, item, session)


@item_router.post('/bulk', status_code=status.HTTP_201_CREATED)
async def items_add(items: list[ItemAdd], session: SessionDep):
    return await ItemService.add_all_items(items, session)

