def test_history_empty(client):
    res = client.get("/api/history")
    assert res.status_code == 200
    body = res.get_json()
    assert body["history"] == []
    assert body["total"] == 0


def test_history_with_limit(client):
    res = client.get("/api/history?limit=5")
    assert res.status_code == 200
    body = res.get_json()
    assert body["per_page"] == 5
