"""
Search endpoints.

Provides an API endpoint that allows users to search
through the stored scraped items.
"""

from flask import Blueprint, jsonify, request

from services.storage import load_items

search_bp = Blueprint("search", __name__)


# GET /api/search
# Examples:
# http://127.0.0.1:5000/api/search?q=laptop
# http://127.0.0.1:5000/api/search?q=laptop&market=Retail%20Goods
# http://127.0.0.1:5000/api/search?q=laptop&page=2&per_page=10
@search_bp.route("/api/search", methods=["GET"])
def search_items():
    query = request.args.get("q", "").lower()
    market = request.args.get("market", "").lower()

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "page and per_page must be positive integers"}), 400
    if per_page > 100:
        return jsonify({"error": "per_page cannot exceed 100"}), 400

    items = load_items()
    results = []

    for item in items:
        # Use .get() defensively so a malformed/partial item can't 500 the
        # whole search instead of just being skipped.
        name = str(item.get("name", "")).lower()
        item_market = str(item.get("market", "")).lower()

        matches_name = query in name
        matches_market = market == "" or item_market == market

        if matches_name and matches_market:
            results.append(item)

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "items": results[start:end],
        "total": len(results),
        "page": page,
        "per_page": per_page
    })
