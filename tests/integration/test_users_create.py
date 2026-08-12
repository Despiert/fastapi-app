async def test_user_add_success(client, session):
    response = await client.post('/users/user', json={"username": "Test Name", "email": "test@example.com", "password": "securePass123"})
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == 'Test Name'
    assert data['email'] == 'test@example.com'
    assert data['id'] == 1