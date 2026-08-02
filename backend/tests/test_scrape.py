def test_scrape_status_endpoint(client):
    res = client.get("/api/scrape/status")
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "ok"


def test_scrape_rejects_unknown_market(client):
    res = client.post("/api/scrape?market=NotAMarket")
    assert res.status_code == 400
    assert res.get_json()["status"] == "error"
