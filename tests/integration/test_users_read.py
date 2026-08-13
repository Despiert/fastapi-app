async def test_user_get_all_empty(client, session):
    response = await client.get('/users/all')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

async def test_user_get_all_success(client, session):
    await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    await client.post('/users/user', json={"username": "User2", "email": "test2@example.com", "password": "securePass123"})

    response = await client.get('/users/all')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_user_get_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.get('/users/1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['username'] == 'User1'
    assert data['email'] == 'test@example.com'

async def test_user_get_not_found(client, session):
    response = await client.get('/users/1')
    assert response.status_code == 404

async def test_user_get_by_email_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.get('/users/email/test@example.com')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['username'] == 'User1'
    assert data['email'] == 'test@example.com'

async def test_user_get_by_email_not_found(client, session):
    response = await client.get('/users/email/test@example.com')
    assert response.status_code == 404