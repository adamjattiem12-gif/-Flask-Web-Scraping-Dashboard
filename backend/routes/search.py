"""
Search endpoints.
"""

from flask import Blueprint, jsonify, request

from services.storage import load_items

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search", methods=["GET"])
def search_items():

    query = request.args.get("q", "").lower()

    items = load_items()

    if query == "":
        return jsonify(items)

    results = []

    for item in items:

        if query in item["name"].lower():

            results.append(item)

    return jsonify(results)