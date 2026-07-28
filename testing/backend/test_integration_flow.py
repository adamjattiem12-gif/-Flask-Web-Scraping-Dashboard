"""
Integration-style tests that exercise several backend pieces together:
storage -> /api/items -> /api/statistics -> /api/history, wired up the
same way routes/scrape.py wires them (minus the actual network calls,
since scrapers.* cannot currently be imported - see TC-BE-16/17).
"""
from datetime import datetime

from flask import Flask
import services.storage as storage
from routes.items import items_bp
from routes.statistics import statistics_bp
from routes.history import history_bp
from routes.websites import website_bp


def make_full_client():
    app = Flask(__name__)
    app.register_blueprint(items_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(website_bp)
    return app.test_client()


def test_simulated_scrape_updates_items_statistics_and_history(isolated_data):
    client = make_full_client()

    # Step 1: simulate what routes/scrape.py would produce and persist
    new_batch = [
        {"id": 1, "name": "Simulated Widget", "price": 12.5,
         "price_display": "$12.50", "currency": "USD", "source": "test",
         "market": "Retail Goods", "scraped_at": datetime.now().isoformat(),
         "extra": {"rating": 5, "review_count": 2}},
        {"id": "sim-coin", "name": "SimCoin", "price": 100.0,
         "price_display": "$100.00", "currency": "USD", "source": "test",
         "market": "Digital Assets", "scraped_at": datetime.now().isoformat(),
         "extra": {"rating": 1, "review_count": 0}},
    ]
    storage.save_items(new_batch)
    storage.add_history({
        "timestamp": datetime.now().isoformat(),
        "scraper_type": "ecommerce", "market": "Retail Goods",
        "items_found": 1, "success": True,
    })
    storage.add_history({
        "timestamp": datetime.now().isoformat(),
        "scraper_type": "crypto", "market": "Digital Assets",
        "items_found": 1, "success": True,
    })

    # Step 2: /api/items reflects the new snapshot, not the old 21 items
    items_resp = client.get("/api/items").get_json()
    assert items_resp["total"] == 2
    names = {i["name"] for i in items_resp["items"]}
    assert names == {"Simulated Widget", "SimCoin"}

    # Step 3: /api/statistics (fallback calc) reflects the new snapshot
    stats_resp = client.get("/api/statistics").get_json()
    assert stats_resp["total_items"] == 2
    assert "Retail Goods" in stats_resp["markets"]
    assert "Digital Assets" in stats_resp["markets"]

    # Step 4: /api/history shows the two new records appended
    history_resp = client.get("/api/history").get_json()
    assert history_resp[-2:] == [
        r for r in storage.load_history()[-2:]
    ]
    assert history_resp[-1]["market"] == "Digital Assets"

    # Step 5: the previous 21-item snapshot was preserved in items_history.json
    versioned = storage.load_items_history()
    assert len(versioned) == 1
    assert len(versioned[0]["items"]) == 21


def test_websites_registry_feeds_scrape_url_resolution_logic(isolated_data):
    """routes/scrape.py resolves target URLs by matching website['market'];
    confirm the registry actually contains both markets it depends on."""
    client = make_full_client()
    sites = client.get("/api/websites").get_json()
    markets = {s["market"] for s in sites}
    assert "E-Commerce" in markets
    assert "Cryptocurrency" in markets
