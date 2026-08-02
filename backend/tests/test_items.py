def test_get_items_empty(client):
    res = client.get("/api/items")
    assert res.status_code == 200
    body = res.get_json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["page"] == 1


def test_get_items_rejects_bad_pagination(client):
    res = client.get("/api/items?page=0")
    assert res.status_code == 400

    res = client.get("/api/items?per_page=abc")
    assert res.status_code == 400

    res = client.get("/api/items?per_page=1000")
    assert res.status_code == 400


def test_get_items_market_filter(client):
    res = client.get("/api/items?market=Retail Goods")
    assert res.status_code == 200
    body = res.get_json()
    assert all(item["market"] == "Retail Goods" for item in body["items"])
