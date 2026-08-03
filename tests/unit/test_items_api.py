import pytest



async def test_item_add_success(client, session):
    response = await client.post('/items/item', json={"name": "Test Item","price": 100, "stock_quantity": 15})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Test Item'
    assert data['price'] == 100
    assert data['stock_quantity'] == 15

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