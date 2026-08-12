async def test_item_delete_not_found(client, session):
    response = await client.delete('/items/1')
    assert response.status_code == 404

async def test_item_delete_success(client, session):
    create = await client.post('/items/item', json={"name": "Item1", "price": 100, "stock_quantity": 10})
    assert create.status_code == 201

    response = await client.delete('/items/1')
    assert response.status_code == 200

    resp = await client.delete('/items/1')
    assert resp.status_code == 404