"""
Search endpoints.

Provides an API endpoint for searching stored items.
"""

from flask import Blueprint, jsonify, request
from services.storage import load_items

# Create a Blueprint for search routes
search_bp = Blueprint("search", __name__)

# GET /api/search?q=<search_term>
@search_bp.route("/api/search", methods=["GET"])
def search_items():

    # Get the search query from the URL
    # Example: /api/search?q=laptop
    query = request.args.get("q", "").lower()

    # Load all stored items
    items = load_items()

    # If no search term is entered, return every item
    if query == "":
        return jsonify(items)

    # Store matching results
    results = []

    # Search through each item
    for item in items:

        # Check if the search term appears in the item's name
        if query in item.get("name", "").lower():

            # Add matching item to the results
            results.append(item)

    # Return the matching items as JSON
    return jsonify(results)