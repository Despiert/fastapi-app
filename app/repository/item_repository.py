from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.item import ItemAdd, ItemUpdate
from app.models.items import Item


class ItemRepository:
    @classmethod
    async def add_one(cls, data: ItemAdd, session: AsyncSession) -> Item:
        item_dict = data.model_dump()
        item = Item(**item_dict)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @classmethod
    async def find_all(cls, session: AsyncSession):
        stmt = select(Item)
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items

    @classmethod
    async def find_by_name(cls, name: str, session: AsyncSession):
        stmt = select(Item).where(Item.name == name)
        result = await session.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            return item
        return None

    @classmethod
    async def find_by_id(cls, item_id: int, session: AsyncSession):
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        return existing

    @classmethod
    async def search_items(cls, item_search: str, session: AsyncSession):
        stmt = select(Item).where(Item.name.contains(item_search))
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items

    @classmethod
    async def add_all_items(cls, items: list[ItemAdd], session: AsyncSession):
        added = []
        skipped = []
        for item in items:
            stmt = select(Item).where(Item.name == item.name)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            if existing:
                skipped.append({'name': item.name, "reason": "Уже существует"})
                continue
            new_item = Item(**item.model_dump())
            added.append(new_item)
            session.add(new_item)
            await session.commit()
        return {'added': added, 'skipped': skipped}

    @classmethod
    async def patch_item(cls, item: Item, data_item: ItemUpdate, session: AsyncSession):
        for key, value in data_item.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item