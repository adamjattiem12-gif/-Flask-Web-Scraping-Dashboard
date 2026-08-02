def test_get_websites_seeds_defaults(client):
    res = client.get("/api/websites")
    assert res.status_code == 200
    body = res.get_json()
    assert len(body) == 2
    assert all("id" in w for w in body)


def test_create_website_success(client):
    # Seed the 2 default websites first (they're lazily created on first read)
    baseline_count = len(client.get("/api/websites").get_json())

    payload = {
        "name": "Test News Site",
        "url": "https://example.com/news",
        "market": "Retail Goods",
    }
    res = client.post("/api/websites", json=payload)
    assert res.status_code == 201
    body = res.get_json()
    assert body["name"] == "Test News Site"
    assert "id" in body

    # New site should now appear in the full list
    res = client.get("/api/websites")
    assert len(res.get_json()) == baseline_count + 1


def test_create_website_missing_fields(client):
    res = client.post("/api/websites", json={"name": "No URL or market"})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_website_invalid_market(client):
    res = client.post("/api/websites", json={
        "name": "Bad Market", "url": "https://example.com", "market": "Not A Market"
    })
    assert res.status_code == 400


def test_create_website_invalid_url_scheme(client):
    res = client.post("/api/websites", json={
        "name": "Bad URL", "url": "ftp://example.com", "market": "Retail Goods"
    })
    assert res.status_code == 400


def test_delete_website_success(client):
    create_res = client.post("/api/websites", json={
        "name": "Temp Site", "url": "https://example.com", "market": "Digital Assets"
    })
    new_id = create_res.get_json()["id"]

    del_res = client.delete(f"/api/websites/{new_id}")
    assert del_res.status_code == 200
    assert del_res.get_json()["deleted"] is True

    res = client.get("/api/websites")
    assert all(w["id"] != new_id for w in res.get_json())


def test_delete_website_not_found(client):
    res = client.delete("/api/websites/99999")
    assert res.status_code == 404
