from flask import Blueprint, jsonify
from services.storage import load_items, load_websites, load_history, load_statistics
from datetime import datetime

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/api/statistics')
def get_statistics():
    # Use persisted statistics if available (written by the scraper on each run)
    persisted = load_statistics()
    if persisted:
        return jsonify(persisted)

    # ---- Fallback: calculate dynamically when statistics.json is empty ----
    all_items = load_items()
    websites = load_websites()
    history = load_history()

    total_items = len(all_items)
    active_sites = len(websites)

    # Calculate success rate from history
    if history:
        successful = sum(
            1 for record in history
            if record.get('success') is True or record.get('status') == 'Success'
        )
        success_rate = round((successful / len(history)) * 100, 1)
    else:
        success_rate = 100.0

    # Determine last scrape timestamp
    if all_items:
        last_scrape = max(
            (item.get('scraped_at', '') for item in all_items),
            default=datetime.now().isoformat()
        )
    elif history:
        last_scrape = max(
            (record.get('timestamp', '') for record in history),
            default=datetime.now().isoformat()
        )
    else:
        last_scrape = datetime.now().isoformat()

    # Group items by market
    markets = {}
    for item in all_items:
        market_name = item.get('market', 'Unknown')
        if market_name not in markets:
            markets[market_name] = []
        markets[market_name].append(item)

    markets_stats = {}
    for market_name, market_items in markets.items():
        prices = [item['price'] for item in market_items if 'price' in item]
        avg_price = round(sum(prices) / len(prices), 2) if prices else 0.0
        last_updated = max(
            (item.get('scraped_at', '') for item in market_items),
            default=datetime.now().isoformat()
        )
        markets_stats[market_name] = {
            "item_count": len(market_items),
            "avg_price": avg_price,
            "last_updated": last_updated
        }

    return jsonify({
        "total_items": total_items,
        "active_sites": active_sites,
        "success_rate": success_rate,
        "last_scrape": last_scrape,
        "markets": markets_stats
    })
