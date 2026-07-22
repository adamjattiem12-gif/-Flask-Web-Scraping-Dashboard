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
@search_bp.route("/api/search", methods=["GET"])
def search_items():

    # Retrieve the search term from the URL
    # If no search term is provided, use an empty string
    query = request.args.get("q", "").lower()

    # Load all previously stored items
    items = load_items()

    # If the search box is empty,
    # return all stored items
    if query == "":
        return jsonify(items)

    # Create an empty list to store matching items
    results = []

    # Loop through every stored item
    for item in items:

        # Check if the search term appears
        # in the item's name (case-insensitive)
        if query in item["name"].lower():

            # Add the matching item to the results list
            results.append(item)

    # Return the matching items as JSON
    return jsonify(results)