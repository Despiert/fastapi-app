async def test_item_patch_not_found(client, session):
    item_id = 1
    response = await client.patch(f'/items/{item_id}', json={"price": 10})
    assert response.status_code == 404

async def test_item_patch_success(client, session):
    await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})

    item_id = 1
    response = await client.patch(f'/items/{item_id}', json={"price": 50})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Item1'
    assert data['price'] == 50
    assert data['stock_quantity'] == 10
    assert data['description'] == 'No description'

async def test_item_patch_multiple_fields(client, session):
    await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})

    item_id = 1
    response = await client.patch(f'/items/{item_id}', json={"price": 50, "stock_quantity": 20, "description": "Test description"})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Item1'
    assert data['price'] == 50
    assert data['stock_quantity'] == 20
    assert data['description'] == 'Test description'