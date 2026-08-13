async def test_user_add_success(client, session):
    response = await client.post('/users/user', json={"username": "Test Name", "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == 'Test Name'
    assert data['email'] == 'test@example.com'
    assert data['id'] == 1

async def test_user_add_duplicate_email(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.post('/users/user', json={"username": "User2", "email": "test@example.com", "password": "anotherPass123"})
    assert response.status_code == 409

async def test_user_add_short_username(client):
    response = await client.post('/users/user', json={"username": "U1", "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 422

async def test_user_add_long_username(client):
    response = await client.post('/users/user', json={"username": "U" * 31, "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 422

async def test_user_add_short_password(client):
    response = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "sPass12"})
    assert response.status_code == 422

async def test_user_add_long_password(client):
    response = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "P" * 31})
    assert response.status_code == 422

async def test_user_add_invalid_email(client):
    response = await client.post('/users/user', json={"username": "User1", "email": "testexample.com", "password": "securePass123"})
    assert response.status_code == 422

async def test_user_add_missing_field(client):
    response = await client.post('/users/user', json={"username": "User1", "password": "securePass123"})
    assert response.status_code == 422

async def test_user_add_extra_field(client):
    response = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123", "is_active": True})
    assert response.status_code == 422