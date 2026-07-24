from flask import Blueprint, request, jsonify

items_bp = Blueprint('items', __name__)

MOCK_ITEMS = [
    {
        "id": 1,
        "name": "Asus VivoBook X441NA-GA190",
        "price": 295.99,
        "price_display": "$295.99",
        "currency": "USD",
        "source": "WebScraper.io E-Commerce",
        "market": "Retail Goods",
        "scraped_at": "2026-07-20T14:30:00",
        "extra": {"rating": 4, "review_count": 14}
    },
    {
        "id": 2,
        "name": "Bitcoin",
        "price": 62450.00,
        "price_display": "$62,450.00",
        "currency": "USD",
        "source": "CoinGecko",
        "market": "Digital Assets",
        "scraped_at": "2026-07-20T14:30:00",
        "extra": {}
    }
]

@items_bp.route('/api/items')
def get_items():
    market = request.args.get('market')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    items = MOCK_ITEMS
    if market:
        items = [i for i in items if i['market'] == market]

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "per_page": per_page
    })