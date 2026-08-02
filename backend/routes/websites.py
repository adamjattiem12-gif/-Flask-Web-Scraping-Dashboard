"""
Website endpoints.

Provides API endpoints for viewing, registering, and removing the
target websites the scraping engine draws from.
"""

from flask import Blueprint, jsonify, request

from services.storage import load_websites, add_website, delete_website

website_bp = Blueprint("websites", __name__)

VALID_MARKETS = ("Retail Goods", "Digital Assets")


# GET /api/websites
@website_bp.route("/api/websites", methods=["GET"])
def get_websites():
    """Return all registered websites stored in the application."""
    websites = load_websites()
    return jsonify(websites)


# POST /api/websites
# Body: {"name": "...", "url": "...", "market": "Retail Goods", "path_keywords": ["optional", "list"]}
@website_bp.route("/api/websites", methods=["POST"])
def create_website():
    """Register a new target website for scraping."""
    body = request.get_json(silent=True) or {}

    name = (body.get("name") or "").strip()
    url = (body.get("url") or "").strip()
    market = (body.get("market") or "").strip()
    path_keywords = body.get("path_keywords")

    if not name or not url or not market:
        return jsonify({"error": "name, url, and market are all required"}), 400

    if market not in VALID_MARKETS:
        return jsonify({"error": f"market must be one of {list(VALID_MARKETS)}"}), 400

    if not (url.startswith("http://") or url.startswith("https://")):
        return jsonify({"error": "url must start with http:// or https://"}), 400

    if path_keywords is not None and not isinstance(path_keywords, list):
        return jsonify({"error": "path_keywords must be a list of strings if provided"}), 400

    website = add_website(name, url, market, path_keywords)
    return jsonify(website), 201


# DELETE /api/websites/<id>
@website_bp.route("/api/websites/<int:website_id>", methods=["DELETE"])
def remove_website(website_id):
    """Remove a registered website by id."""
    deleted = delete_website(website_id)
    if not deleted:
        return jsonify({"error": f"No website found with id {website_id}"}), 404
    return jsonify({"deleted": True, "id": website_id}), 200
