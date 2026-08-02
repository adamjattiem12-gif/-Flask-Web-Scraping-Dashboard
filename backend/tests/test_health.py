def test_health_ok(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_health_check_requires_params(client):
    res = client.get("/api/health/check")
    assert res.status_code == 400
    assert "error" in res.get_json()
