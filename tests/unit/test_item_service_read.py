import pytest

from fastapi import HTTPException
from unittest.mock import patch, AsyncMock, ANY

from app.models.items import Item
from app.services.item_service import ItemService


async def test_item_get_success():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)

    mock_find = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_not_found', mock_raise):
            mock_find.return_value = item1

            result = await ItemService.get_item(1, session=AsyncMock())

    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)

    assert result.id == 1
    assert result.name == 'Item1'
    assert result.price == 100
    assert result.stock_quantity == 10

async def test_item_get_not_found():
    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        mock_find.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await ItemService.get_item(1, session=AsyncMock())

    mock_find.assert_called_once_with(1, ANY)

    assert exc_info.value.status_code == 404
    assert 'не найден' in exc_info.value.detail

async def test_item_get_all_success():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item2 = Item(id=2, name='Item2', price=200, stock_quantity=20)
    item3 = Item(id=3, name='Item3', price=300, stock_quantity=30)

    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_all', mock_find):
        mock_find.return_value = [item1, item2, item3]

        result = await ItemService.get_all(session=AsyncMock())

    mock_find.assert_called_once_with(ANY)

    assert len(result) == 3
    assert result[0].id == 1
    assert result[1].name == 'Item2'
    assert result[2].price == 300
    assert result[2].stock_quantity == 30

async def test_item_get_all_empty():
    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_all', mock_find):
        mock_find.return_value = []

        result = await ItemService.get_all(session=AsyncMock())

    mock_find.assert_called_once_with(ANY)

    assert len(result) == 0

async def test_item_search_success():
    item1 = Item(id=1, name='Test', price=100, stock_quantity=10)

    mock_find = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.search_items', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_not_found', mock_raise):
            mock_find.return_value = [item1]

            result = await ItemService.search_items('Test', session=AsyncMock())

    mock_find.assert_called_once_with('Test', ANY)
    mock_raise.assert_not_called()

    assert result[0].id == 1
    assert result[0].name == 'Test'
    assert result[0].price == 100
    assert result[0].stock_quantity == 10

async def test_item_search_multiple_success():
    item1 = Item(id=1, name='Test', price=100, stock_quantity=10)
    item2 = Item(id=2, name='Test second', price=200, stock_quantity=20)
    item3 = Item(id=3, name='Test3', price=300, stock_quantity=30)

    mock_find = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.search_items', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_not_found', mock_raise):
            mock_find.return_value = [item1, item2, item3]

            result = await ItemService.search_items('Test', session=AsyncMock())

    mock_find.assert_called_once_with('Test', ANY)
    mock_raise.assert_not_called()

    assert len(result) == 3
    assert result[0].id == 1
    assert result[1].name == 'Test second'
    assert result[2].price == 300
    assert result[0].stock_quantity == 10

async def test_item_search_not_found():
    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.search_items', mock_find):
        mock_find.return_value = []

        with pytest.raises(HTTPException) as exc_info:
            await ItemService.search_items('Test', session=AsyncMock())

    mock_find.assert_called_once_with('Test', ANY)

    assert exc_info.value.status_code == 404
    assert 'не найден' in exc_info.value.detail