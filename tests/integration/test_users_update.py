from app.repository.user_repository import SQLUserRepository
from app.utils.hashing import verify_password


async def test_user_update_not_found(client, session):
    response = await client.patch('/users/1', json={"username": "NewName"})
    assert response.status_code == 404

async def test_user_update_username_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201
    data_create = create.json()
    assert data_create['id'] == 1
    assert data_create['username'] == 'User1'
    assert data_create['email'] == 'test@example.com'

    response = await client.patch('/users/1', json={"username": "NewName"})
    assert response.status_code == 200
    data_update = response.json()
    assert data_update['id'] == 1
    assert data_update['username'] == 'NewName'
    assert data_update['email'] == 'test@example.com'

async def test_user_update_email_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201
    data_create = create.json()
    assert data_create['id'] == 1
    assert data_create['username'] == 'User1'
    assert data_create['email'] == 'test@example.com'

    response = await client.patch('/users/1', json={"email": "another@example.com"})
    assert response.status_code == 200
    data_update = response.json()
    assert data_update['id'] == 1
    assert data_update['username'] == 'User1'
    assert data_update['email'] == 'another@example.com'

async def test_user_update_duplicate_email(client, session):
    await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    await client.post('/users/user', json={"username": "User2", "email": "test2@example.com", "password": "securePass123"})

    response = await client.patch('/users/2', json={"email": "test@example.com"})
    assert response.status_code == 409

async def test_user_update_password_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.patch('/users/1', json={"password": "newSecurePass123"})
    assert response.status_code == 200
    repo = SQLUserRepository()
    user = await repo.get_user(1, session)
    assert verify_password("securePass123", user.password) is False
    assert verify_password("newSecurePass123", user.password) is True

async def test_user_replace_not_found(client, session):
    response = await client.put('/users/1', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 404

async def test_user_replace_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201
    data_create = create.json()
    assert data_create['id'] == 1
    assert data_create['username'] == 'User1'
    assert data_create['email'] == 'test@example.com'

    response = await client.put('/users/1', json={"username": "NewName", "email": "test2@example.com", "password": "securePass123"})
    assert response.status_code == 200
    data_update = response.json()
    assert data_update['id'] == 1
    assert data_update['username'] == 'NewName'
    assert data_update['email'] == 'test2@example.com'

async def test_user_replace_duplicate_email(client, session):
    await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    await client.post('/users/user', json={"username": "User2", "email": "test2@example.com", "password": "securePass123"})

    response = await client.put('/users/2', json={"username": "User2", "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 409

async def test_user_replace_missing_field(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.put('/users/1', json={"email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 422

async def test_user_replace_extra_field(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.put('/users/1', json={"username": "User1", "email": "test@example.com", "password": "securePass123", "is_active": True})
    assert response.status_code == 422