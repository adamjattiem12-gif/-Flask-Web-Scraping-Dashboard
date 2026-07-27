from flask import Blueprint, jsonify

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/api/statistics')
def get_statistics():
    return jsonify({
        "total_items": 40,
        "active_sites": 2,
        "success_rate": 96.5,
        "last_scrape": "2026-07-20T14:30:00",
        "markets": {
            "Retail Goods": {
                "item_count": 20,
                "avg_price": 450.00,
                "last_updated": "2026-07-20T14:30:00"
            },
            "Digital Assets": {
                "item_count": 20,
                "avg_price": 28450.00,
                "last_updated": "2026-07-20T14:30:00"
            }
        }
    })