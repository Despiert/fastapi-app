import pytest

from fastapi import HTTPException
from unittest.mock import patch, AsyncMock, ANY

from app.models.items import Item
from app.services.item_service import ItemService
from app.schemas.item import ItemAdd


async def test_item_add_success():
    item_data = ItemAdd(name='Test', price=100, stock_quantity=10)

    mock_find = AsyncMock()
    mock_add = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_name', mock_find):
        with patch('app.repository.item_repository.ItemRepository.add_one', mock_add):
            with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
                mock_find.return_value = None
                expected_item = Item(id=1, name='Test', price=100, stock_quantity=10)
                mock_add.return_value = expected_item

                result = await ItemService.add_new_item(item_data, session=AsyncMock())

    mock_find.assert_called_once_with(item_data.name, ANY)
    mock_add.assert_called_once_with(item_data, ANY)
    mock_raise.assert_not_called()

    assert result == expected_item
    assert result.id == 1
    assert result.name == 'Test'

async def test_item_add_duplicate_name():
    item_data = ItemAdd(name='Test', price=100, stock_quantity=10)
    mock_find = AsyncMock()
    mock_add = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_name', mock_find):
        with patch('app.repository.item_repository.ItemRepository.add_one', mock_add):
            expected_item = Item(id=1, name='Test', price=100, stock_quantity=10)
            mock_find.return_value = expected_item

            with pytest.raises(HTTPException) as exc_info:
                await ItemService.add_new_item(item_data, session=AsyncMock())

    mock_find.assert_called_once_with(item_data.name, ANY)
    mock_add.assert_not_called()

    assert exc_info.value.status_code == 409
    assert 'внесен в базу' in exc_info.value.detail

async def test_item_add_all_success():
    items = [
        ItemAdd(name='Item1', price=100, stock_quantity=10),
        ItemAdd(name='Item2', price=200, stock_quantity=20)
    ]
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item2 = Item(id=2, name='Item2', price=200, stock_quantity=20)

    mock_adds = AsyncMock()
    mock_adds.return_value = {"added": [item1, item2], "skipped": []}

    with patch('app.repository.item_repository.ItemRepository.add_all_items', mock_adds):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists') as mock_raise:
            result = await ItemService.add_all_items(items, session=AsyncMock())

    mock_adds.assert_called_once_with(items, ANY)
    mock_raise.assert_not_called()

    assert len(result['added']) == 2
    assert len(result['skipped']) == 0
    assert result['added'][0].id == 1
    assert result['added'][0].name == 'Item1'
    assert result['added'][1].price == 200
    assert result['added'][1].stock_quantity == 20

async def test_item_add_all_partial_skip():
    items = [
        ItemAdd(name='Item1', price=100, stock_quantity=10),
        ItemAdd(name='Item2', price=200, stock_quantity=20),
        ItemAdd(name='Item3', price=300, stock_quantity=30)
    ]
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item2 = Item(id=2, name='Item2', price=200, stock_quantity=20)
    item3 = Item(id=3, name='Item3', price=300, stock_quantity=30)

    mock_adds = AsyncMock()
    mock_adds.return_value = {"added": [item1, item3], "skipped": [item2]}

    with patch('app.repository.item_repository.ItemRepository.add_all_items', mock_adds):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists') as mock_raise:
            result = await ItemService.add_all_items(items, session=AsyncMock())

    mock_adds.assert_called_once_with(items, ANY)
    mock_raise.assert_not_called()

    assert len(result['added']) == 2
    assert len(result['skipped']) == 1
    assert result['added'][0].id == 1
    assert result['added'][1].name == 'Item3'
    assert result['skipped'][0].price == 200
    assert result['skipped'][0].stock_quantity == 20

async def test_item_add_all_full_duplicate():
    items = [
        ItemAdd(name='Item1', price=100, stock_quantity=10),
        ItemAdd(name='Item2', price=200, stock_quantity=20)
    ]
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item2 = Item(id=2, name='Item2', price=200, stock_quantity=20)

    mock_adds = AsyncMock()
    mock_adds.return_value = {"added": [], "skipped": [item1, item2]}
    result = mock_adds.return_value

    with patch('app.repository.item_repository.ItemRepository.add_all_items', mock_adds):
        with pytest.raises(HTTPException) as exc_info:
            await ItemService.add_all_items(items, session=AsyncMock())

    mock_adds.assert_called_once_with(items, ANY)

    assert exc_info.value.status_code == 409
    assert 'внесен в базу' in exc_info.value.detail
    assert result['added'] == []
    assert len(result['skipped']) == 2
    assert result['skipped'][0].id == 1
    assert result['skipped'][0].name == 'Item1'
    assert result['skipped'][1].price == 200
    assert result['skipped'][1].stock_quantity == 20