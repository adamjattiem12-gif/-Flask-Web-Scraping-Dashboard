def test_statistics_shape(client):
    res = client.get("/api/statistics")
    assert res.status_code == 200
    body = res.get_json()
    for key in ("total_items", "active_sites", "success_rate", "last_scrape", "markets"):
        assert key in body
