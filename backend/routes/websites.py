"""
Website endpoints.

Provides API endpoints for working with the list
of registered websites stored by the application.
"""

# Import Flask modules
# Blueprint is used to organize website-related routes
# jsonify converts Python objects into JSON responses
from flask import Blueprint, jsonify

# Import the function that loads registered websites
# from the storage layer
from services.storage import load_websites

# Create a Blueprint for all website-related routes
website_bp = Blueprint("websites", __name__)


# GET /api/websites
# Example:
# http://127.0.0.1:5000/api/websites
@website_bp.route("/api/websites", methods=["GET"])
def get_websites():
    """
    Return all registered websites stored in the application.
    """

    # Load the registered websites from storage
    websites = load_websites()

    # Return the websites as a JSON response
    return jsonify(websites)