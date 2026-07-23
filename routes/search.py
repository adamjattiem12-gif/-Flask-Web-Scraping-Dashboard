"""
Search endpoints.

Provides an API endpoint that allows users to search
through the stored scraped items.
"""

# Import Flask modules
# Blueprint is used to organize routes
# jsonify converts Python objects into JSON responses
# request allows access to URL query parameters
from flask import Blueprint, jsonify, request

# Import the function that loads stored items from storage
from services.storage import load_items

# Create a Blueprint for all search-related routes
search_bp = Blueprint("search", __name__)


# GET /api/search
# Example:
# http://127.0.0.1:5000/api/search?q=laptop
# http://127.0.0.1:5000/api/search?q=laptop&market=Retail%20Goods
@search_bp.route("/api/search", methods=["GET"])
def search_items():

    # Retrieve the search term from the URL
    # If no search term is provided, use an empty string
    query = request.args.get("q", "").lower()

    # Retrieve the optional market parameter
    # If no market is provided, use an empty string
    market = request.args.get("market", "").lower()

    # Load all stored items
    items = load_items()

    # Store matching items
    results = []

    # Loop through every stored item
    for item in items:

        # Check if the search query is in the product name
        matches_name = query in item["name"].lower()

        # Check if the market matches
        # If no market is supplied, accept all markets
        matches_market = (
            market == "" or
            item["market"].lower() == market
        )

        # Add the item if both conditions are met
        if matches_name and matches_market:
            results.append(item)

    # Return all matching items as JSON
    return jsonify(results)