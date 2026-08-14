import pytest

from fastapi import HTTPException
from unittest.mock import patch, AsyncMock, ANY

from app.models.items import Item
from app.services.item_service import ItemService


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