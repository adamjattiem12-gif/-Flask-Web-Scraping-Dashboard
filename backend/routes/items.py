from flask import Blueprint, request, jsonify
from services.storage import load_items

items_bp = Blueprint('items', __name__)

@items_bp.route('/api/items')
def get_items():
    market = request.args.get('market')

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "page and per_page must be positive integers"}), 400

    if per_page > 100:
        return jsonify({"error": "per_page cannot exceed 100"}), 400

    items = load_items()
    if market:
        items = [i for i in items if i['market'] == market]

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "per_page": per_page
    })
