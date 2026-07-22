"""
Website endpoints.
"""

from flask import Blueprint, jsonify

from services.storage import load_websites

website_bp = Blueprint("websites", __name__)


@website_bp.route("/api/websites", methods=["GET"])
def get_websites():
    """
    Return every registered website.
    """

    websites = load_websites()

    return jsonify(websites)