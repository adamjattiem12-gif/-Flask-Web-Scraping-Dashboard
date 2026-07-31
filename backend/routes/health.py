from flask import Blueprint, request, jsonify
from utils.validators import health_check
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health')
def health():
    return {"status": "ok"}

@health_bp.route('/api/health/check')
def check_endpoint():
    url = request.args.get('url')
    scraper_type = request.args.get('type')
    
    if not url or not scraper_type:
        return jsonify({"healthy": False, "error": "Missing url or type"}), 400

    is_healthy = health_check(url, scraper_type)
    return jsonify({
        "healthy": is_healthy,
        "url": url,
        "type": scraper_type,
        "checked_at": datetime.now().isoformat()
    })