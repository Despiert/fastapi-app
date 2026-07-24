import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.item import ItemAdd, ItemUpdate
from app.repository.item_repository import ItemRepository
from app.configs.constants import ENTITY_ITEM
from app.utils.exceptions import ErrorHandler


logger = logging.getLogger(__name__)


class ItemService:
    @staticmethod
    async def add_new_item(item_date: ItemAdd, session: AsyncSession):
        logger.info(f'Попытка добавления товара: "{item_date.name}"')
        existing = await ItemRepository.find_by_name(item_date.name, session)
        if existing:
            raise ErrorHandler.raise_already_exists(ENTITY_ITEM, item_date.name)
        item_model = await ItemRepository.add_one(item_date, session)
        logger.info(f'Товар "{item_date.name}" добавлен с id "{item_model.id}"')
        return item_model

    @staticmethod
    async def get_item(item_id: int, session: AsyncSession):
        logger.info(f'Попытка поиска товара с id: "{item_id}"')
        item = await ItemRepository.find_by_id(item_id, session)
        if item is None:
            raise ErrorHandler.raise_not_found(ENTITY_ITEM, item_id)
        logger.info(f'Товар с id: "{item_id}" найден')
        return item

    @staticmethod
    async def get_all(session: AsyncSession):
        logger.info(f'Попытка поиска товаров')
        items = await ItemRepository.find_all(session)
        logger.info(f'Найдено товаров "{len(items)}"')
        return items

    @staticmethod
    async def del_item(item_id: int, session: AsyncSession):
        logger.info(f'Попытка поиска товара с id: "{item_id}"')
        existing = await ItemRepository.find_by_id(item_id, session)
        if existing:
            await session.delete(existing)
            await session.commit()
            logger.info(f'Товар с id: "{item_id}" удален из базы')
            return 'Товар удален из базы данных'
        raise ErrorHandler.raise_not_found(ENTITY_ITEM, item_id)

    @staticmethod
    async def patch_item(item_id: int, data_item: ItemUpdate, session: AsyncSession):
        logger.info(f'Попытка поиска товара с id: "{item_id}"')
        existing = await ItemRepository.find_by_id(item_id, session)
        if existing:
            for key, value in data_item.model_dump(exclude_unset=True).items():
                setattr(existing, key, value)
            session.add(existing)
            await session.commit()
            await session.refresh(existing)
            logger.info(f'Товар с id: "{item_id}" изменен')
            return existing
        raise ErrorHandler.raise_not_found(ENTITY_ITEM, item_id)

    @staticmethod
    async def search_items(item_search: str, session: AsyncSession):
        logger.info(f'Попытка поиска товара "{item_search}"')
        items = await ItemRepository.search_items(item_search, session)
        if not items:
            raise ErrorHandler.raise_not_found(ENTITY_ITEM, item_search)
        logger.info(f'Товар "{item_search}" найден')
        return items

    @staticmethod
    async def add_all_items(items: list[ItemAdd], session: AsyncSession):
        logger.info('Добавление товаров')
        result = await ItemRepository.add_all_items(items, session)
        if result.get('added'):
            logger.info(f'Товары добавлены "{len(result["added"])}"')
            return result
        raise ErrorHandler.raise_already_exists(ENTITY_ITEM)

