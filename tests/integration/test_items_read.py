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

async def test_item_get_not_found(client, session, item_id: int = 1):
    response = await client.get(f'/items/{item_id}')
    assert response.status_code == 404

async def test_item_get_success(client, session, item_id: int = 2):
    await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})
    await client.post('/items/item', json={"name": "Item2", "price": 200, "stock_quantity": 5})

    response = await client.get(f'/items/{item_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Item2'
    assert data['description'] == 'No description'
    assert data['price'] == 200
    assert data['stock_quantity'] == 5

async def test_item_search_not_found(client, session):
    response = await client.get('/items/search?item_search=Ноутбук')
    assert response.status_code == 404

async def test_item_search_success(client, session):
    await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})
    await client.post('/items/item', json={"name": "Ноутбук", "price": 500, "stock_quantity": 3})

    response = await client.get('/items/search?item_search=Ноутбук')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == "Ноутбук"
    assert data[0]['price'] == 500
    assert data[0]['stock_quantity'] == 3
    assert data[0]['description'] == 'No description'

async def test_item_search_multiple(client, session):
    await client.post('/items/item', json={"name": "Ноутбук", "price": 500, "stock_quantity": 3})
    await client.post('/items/item', json={"name": "Item2", "price": 100, "stock_quantity": 10})
    await client.post('/items/item', json={"name": "Ноутбук Pro", "price": 700, "stock_quantity": 2, "description": "test description"})

    response = await client.get('/items/search?item_search=Ноутбук')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    assert data[0]['name'] == "Ноутбук"
    assert data[0]['price'] == 500
    assert data[0]['stock_quantity'] == 3
    assert data[0]['description'] == 'No description'

    assert data[1]['name'] == "Ноутбук Pro"
    assert data[1]['price'] == 700
    assert data[1]['stock_quantity'] == 2
    assert data[1]['description'] == 'test description'