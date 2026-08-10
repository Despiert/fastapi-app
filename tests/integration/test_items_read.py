async def test_item_all_empty(client, session):
    response = await client.get('/items/all')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

async def test_item_all_success(client, session):
    await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})
    await client.post('/items/item', json={"name": "Item2", "price": 10, "stock_quantity": 1})

    response = await client.get('/items/all')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
