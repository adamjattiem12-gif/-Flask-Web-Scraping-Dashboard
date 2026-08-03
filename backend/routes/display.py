from flask import Blueprint, jsonify
from services.storage import load_items

display_bp = Blueprint("display", __name__)

current_items = []

def set_current_items(items):
    global current_items
    current_items = items

@display_bp.route("/api/display-items", methods=["GET"])
def get_display_items():
    return jsonify(current_items)


@display_bp.route("/api/display-items", methods=["POST"])
def set_display_items():
    global current_items

    current_items = load_items()

    return jsonify({
        "message": "Display updated.",
        "count": len(current_items)
    })

@display_bp.route("/api/display-items/clear", methods=["POST"])
def clear_display():
    global current_items

    current_items = []

    return jsonify({
        "message": "Display cleared."
    })