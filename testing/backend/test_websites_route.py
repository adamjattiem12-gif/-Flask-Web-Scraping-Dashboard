from flask import Flask
from routes.websites import website_bp


def make_client():
    app = Flask(__name__)
    app.register_blueprint(website_bp)
    return app.test_client()


def test_get_websites_returns_seeded_list(isolated_data):
    resp = make_client().get("/api/websites")
    body = resp.get_json()
    assert resp.status_code == 200
    assert len(body) == 2
    names = {w["market"] for w in body}
    assert names == {"E-Commerce", "Cryptocurrency"}


def test_get_websites_auto_seeds_defaults_when_file_missing(isolated_data):
    (isolated_data / "websites.json").unlink()
    resp = make_client().get("/api/websites")
    body = resp.get_json()
    assert len(body) == 2
