import pytest

from fastapi import HTTPException
from unittest.mock import patch, AsyncMock, ANY

from app.models.items import Item
from app.services.item_service import ItemService
from app.schemas.item import ItemAdd, ItemUpdate


async def test_item_add_success():
    item_data = ItemAdd(name='Test', price=100, stock_quantity=10)

    mock_find = AsyncMock()
    mock_add = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_name', mock_find):
        with patch('app.repository.item_repository.ItemRepository.add_one', mock_add):
            mock_find.return_value = None
            expected_item = Item(id=1, name='Test', price=100, stock_quantity=10)
            mock_add.return_value = expected_item

            result = await ItemService.add_new_item(item_data, session=AsyncMock())

            mock_find.assert_called_once_with(item_data.name, ANY)
            mock_add.assert_called_once_with(item_data, ANY)

            with patch('app.utils.exceptions.ErrorHandler.raise_already_exists') as mock_raise:
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

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
            mock_find.return_value = item1

            await ItemService.patch_item(1, item_data, session=AsyncMock())

    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)

    assert item1.id == 1
    assert item1.name == 'Test'
    assert item1.price == 100
    assert item1.stock_quantity == 111

async def test_item_patch_empty():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)
    item_data = ItemUpdate()

    mock_find = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
            mock_find.return_value = item1

            await ItemService.patch_item(1, item_data, session=AsyncMock())

    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)

    assert item1.id == 1
    assert item1.name == 'Item1'
    assert item1.price == 100
    assert item1.stock_quantity == 10

async def test_item_delete_success():
    item1 = Item(id=1, name='Item1', price=100, stock_quantity=10)

    mock_find = AsyncMock()
    mock_raise = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        with patch('app.utils.exceptions.ErrorHandler.raise_not_found', mock_raise):
            mock_find.return_value = item1

            result = await ItemService.del_item(1, session=AsyncMock())

    mock_raise.assert_not_called()
    mock_find.assert_called_once_with(1, ANY)

    assert 'удален из базы' in result

async def test_item_delete_not_found():
    mock_find = AsyncMock()

    with patch('app.repository.item_repository.ItemRepository.find_by_id', mock_find):
        mock_find.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await ItemService.del_item(1, session=AsyncMock())

    mock_find.assert_called_once_with(1, ANY)

    assert exc_info.value.status_code == 404
    assert 'не найден' in exc_info.value.detail

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