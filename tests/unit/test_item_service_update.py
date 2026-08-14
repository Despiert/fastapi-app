import pytest

from fastapi import HTTPException
from unittest.mock import patch, AsyncMock, ANY

from app.models.items import Item
from app.services.item_service import ItemService
from app.schemas.item import ItemUpdate


async def test_item_patch_not_found():
    item_data = ItemUpdate(name='Test', stock_quantity=10)

    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        mock_find.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await ItemService.patch_item(1, item_data, session=AsyncMock())

    mock_find.assert_called_once_with(1, ANY)

    assert exc_info.value.status_code == 404
    assert 'не найден' in exc_info.value.detail

async def test_item_patch_success():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item_data = ItemUpdate(name='Test', stock_quantity=111)

    mock_find = AsyncMock()
    mock_raise = AsyncMock()
    mock_patch = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
            with patch('app.repository.item_repository.ItemRepository.patch_item', mock_patch):
                mock_find.return_value = item1
                existing = item1
                existing.name = item_data.name
                existing.stock_quantity = item_data.stock_quantity
                mock_patch.return_value = existing

                await ItemService.patch_item(1, item_data, session=AsyncMock())


    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)
    mock_patch.assert_called_once_with(item1, item_data, ANY)

    assert item1.id == 1
    assert item1.name == 'Test'
    assert item1.price == 100
    assert item1.stock_quantity == 111

async def test_item_patch_empty():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item_data = ItemUpdate()

    mock_find = AsyncMock()
    mock_raise = AsyncMock()
    mock_patch = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
            with patch('app.repository.item_repository.ItemRepository.patch_item', mock_patch):
                mock_find.return_value = item1
                mock_patch.return_value = item1

                await ItemService.patch_item(1, item_data, session=AsyncMock())

    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)
    mock_patch.assert_called_once_with(item1, item_data, ANY)

    assert item1.id == 1
    assert item1.name == 'Item1'
    assert item1.price == 100
    assert item1.stock_quantity == 10