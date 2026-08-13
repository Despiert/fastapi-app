async def test_user_delete_success(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.delete('/users/1')
    assert response.status_code == 200

    get_response = await client.get('/users/1')
    assert get_response.status_code == 404

async def test_user_delete_not_found(client, session):
    response = await client.delete('/users/1')
    assert response.status_code == 404

async def test_user_delete_already_deleted(client, session):
    create = await client.post('/users/user', json={"username": "User1", "email": "test@example.com", "password": "securePass123"})
    assert create.status_code == 201

    response = await client.delete('/users/1')
    assert response.status_code == 200

    second_delete = await client.delete('/users/1')
    assert second_delete.status_code == 404