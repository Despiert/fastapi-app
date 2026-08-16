from unittest.mock import AsyncMock, patch, ANY, Mock

import pytest
from fastapi import HTTPException

from app.models.users import User
from app.schemas.user import UserAdd
from app.services.user_service import UserService


async def test_user_add_success():
    user_data = {"username": "User1", "email": "test@example.com", "password": "securePass123"}

    mock_repo = AsyncMock()
    mock_raise = AsyncMock()
    mock_hash = Mock()
    service = UserService(repository=mock_repo)

    with patch('app.utils.exceptions.ErrorHandler.raise_already_exists', mock_raise):
        with patch('app.services.user_service.hash_password', mock_hash):
            mock_hash.return_value = 'hashed_password'
            mock_repo.find_by_email.return_value = None
            mock_repo.add_user.return_value = UserAdd(**user_data)
            user = UserAdd(**user_data)

            result = await service.add_user(user, session=AsyncMock())

    call_args = mock_repo.add_user.call_args[0][0]

    mock_repo.find_by_email.assert_called_once_with(user_data['email'], ANY)
    mock_repo.add_user.assert_called_once_with(call_args, ANY)
    mock_hash.assert_called_once_with('securePass123')
    mock_raise.assert_not_called()

    assert call_args['password'] == 'hashed_password'
    assert result.username == 'User1'
    assert result.email == 'test@example.com'

async def test_user_add_duplicate_email():
    user_data = {"username": "User1", "email": "test@example.com", "password": "securePass123"}

    mock_repo = AsyncMock()
    service = UserService(repository=mock_repo)

    existing = User(id=1, username='User1', email='test@example.com')
    mock_repo.find_by_email.return_value = existing
    user = UserAdd(**user_data)
    with pytest.raises(HTTPException) as exc_info:
        await service.add_user(user, session=AsyncMock())

    mock_repo.find_by_email.assert_called_once_with(user_data['email'], ANY)
    mock_repo.add_user.assert_not_called()

    assert exc_info.value.status_code == 409
    assert 'внесен в базу' in exc_info.value.detail
    assert user_data['email'] in exc_info.value.detail