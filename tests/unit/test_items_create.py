async def test_item_add_success(client, session):
    response = await client.post('/items/item', json={"name": "Test Item","price": 100, "stock_quantity": 15})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Test Item'
    assert data['price'] == 100
    assert data['stock_quantity'] == 15
    assert data['description'] == 'No description'

async def test_item_add_empty_name(client):
    response = await client.post('/items/item', json={"name":"", "price": 100, "stock_quantity": 1})
    assert response.status_code == 422

async def test_item_add_negative_price(client):
    response = await client.post('/items/item', json={"name": "Test Item", "price": -1, "stock_quantity": 1})
    assert response.status_code == 422

async def test_item_add_missing_field(client):
    response = await client.post('/items/item', json={"price": 100, "stock_quantity": 1})
    assert response.status_code == 422

async def test_item_add_extra_field(client):
    response = await client.post('/items/item', json={"name": "Test Item", "price": 100, "stock_quantity": 1, "extra": "field"})
    assert response.status_code == 422

async def test_item_add_negative_quantity(client):
    response = await client.post('/items/item', json={"name": "Test Item", "price": 100, "stock_quantity": -1})
    assert response.status_code == 422

async def test_items_bulk_success(client, session):
    response = await client.post('items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"name": "Item2", "price": 200, "stock_quantity": 5, "description": "Test Description"},
    ])
    assert response.status_code == 201
    data = response.json()
    assert data['added'][0]['name'] == 'Item1'
    assert data['added'][1]['name'] == "Item2"
    assert data['added'][0]['price'] == 100
    assert data['added'][1]['price'] == 200
    assert data['added'][0]['stock_quantity'] == 10
    assert data['added'][1]['stock_quantity'] == 5
    assert data['added'][1]['description'] == 'Test Description'
    assert data['added'][0]['description'] == 'No description'

async def test_items_bulk_one_item_success(client, session):
    response = await client.post('items/bulk', json=[{"name": "Item1", "price": 100, "stock_quantity": 10}])
    assert response.status_code == 201
    data = response.json()
    assert data['added'][0]['name'] == 'Item1'
    assert data['added'][0]['price'] == 100
    assert data['added'][0]['description'] == 'No description'
    assert data['added'][0]['stock_quantity'] == 10

async def test_items_bulk_empty_name(client):
    response = await client.post('/items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"name": "", "price": 200, "stock_quantity": 5}
    ])
    assert response.status_code == 422

async def test_items_bulk_one_item_empty_name(client):
    response = await client.post('/items/bulk', json=[{"name": "", "price": 100, "stock_quantity": 10}])
    assert response.status_code == 422

async def test_items_bulk_negative_price(client):
    response = await client.post('/items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"name": "Item2", "price": -200, "stock_quantity": 5}
    ])
    assert response.status_code == 422

async def test_items_bulk_one_item_negative_price(client):
    response = await client.post('/items/bulk', json=[{"name": "Item1", "price": -100, "stock_quantity": 10}])
    assert response.status_code == 422

async def test_items_bulk_missing_field(client):
    response = await client.post('/items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"price": -200, "stock_quantity": 5}
    ])
    assert response.status_code == 422

async def test_items_bulk_one_item_missing_field(client):
    response = await client.post('/items/bulk', json=[{"name": "Item1", "stock_quantity": 10}])
    assert response.status_code == 422

async def test_items_bulk_extra_field(client):
    response = await client.post('/items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"name": "Item2", "price": -200, "stock_quantity": 5, "extra": "field"}
    ])
    assert response.status_code == 422

async def test_items_bulk_one_item_extra_field(client):
    response = await client.post('/items/bulk', json=[{"name": "Item1", "price": 100, "stock_quantity": 10, "extra": "field"}])
    assert response.status_code == 422

async def test_items_bulk_negative_quantity(client):
    response = await client.post('/items/bulk', json=[
        {"name": "Item1", "price": 100, "stock_quantity": 10},
        {"name": "Item2", "price": 200, "stock_quantity": -5}
    ])
    assert response.status_code == 422

async def test_items_bulk_one_item_negative_quantity(client):
    response = await client.post('/items/bulk', json=[{"name": "Item1", "price": 100, "stock_quantity": -1}])
    assert response.status_code == 422