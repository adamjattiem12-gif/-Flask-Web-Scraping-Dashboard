"""
History endpoints.

Provides an API endpoint for viewing the application's scraping history.
"""

from flask import Blueprint, jsonify, request

from services.storage import load_history

history_bp = Blueprint("history", __name__)


# GET /api/history
# Examples:
# http://127.0.0.1:5000/api/history
# http://127.0.0.1:5000/api/history?limit=5
# http://127.0.0.1:5000/api/history?market=Retail%20Goods
# http://127.0.0.1:5000/api/history?page=2&per_page=10
@history_bp.route("/api/history", methods=["GET"])
def get_history():
    history = load_history()

    market = request.args.get("market")
    limit = request.args.get("limit", type=int)

    if market:
        market_lower = market.lower()
        history = [
            record for record in history
            if str(record.get("market", "")).lower() == market_lower
        ]

    # Keep oldest-first ordering (as load_history returns it) — the
    # frontend's scrapeStore.fetchHistory() reverses this itself to get
    # newest-first, so reversing here too would double-flip the order.
    if limit:
        # history is oldest-first, so the most recent `limit` records are
        # the tail of the list.
        history = history[-limit:]
        return jsonify({
            "history": history,
            "total": len(history),
            "page": 1,
            "per_page": limit
        })

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", len(history) or 1))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "page and per_page must be positive integers"}), 400

    total = len(history)
    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "history": history[start:end],
        "total": total,
        "page": page,
        "per_page": per_page
    })
