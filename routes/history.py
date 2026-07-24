"""
History endpoints.

Provides an API endpoint for viewing the application's
scraping history.
"""

# Import Flask modules
from flask import Blueprint, jsonify, request

# Import the history storage function
from services.storage import load_history

# Create a Blueprint for history routes
history_bp = Blueprint("history", __name__)


# GET /api/history
# Examples:
# http://127.0.0.1:5000/api/history
# http://127.0.0.1:5000/api/history?limit=5
# http://127.0.0.1:5000/api/history?market=Retail%20Goods
@history_bp.route("/api/history", methods=["GET"])
def get_history():

    # Load all history records
    history = load_history()

    # Optional query parameters
    market = request.args.get("market")
    limit = request.args.get("limit", type=int)

    # Filter by market if supplied
    if market:
        history = [
            record
            for record in history
            if record.get("market") == market
        ]

    # Return only the newest X records if a limit is supplied
    if limit:
        history = history[-limit:]

    # Return the history as JSON
    return jsonify(history)