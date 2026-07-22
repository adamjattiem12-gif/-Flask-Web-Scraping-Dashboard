"""
History endpoints.
"""

from flask import Blueprint, jsonify

from services.storage import load_history

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history", methods=["GET"])
def get_history():
    """
    Return scrape history.
    """

    history = load_history()

    return jsonify(history)