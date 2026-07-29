import logging

from flask import Flask, jsonify
from flask_cors import CORS
from routes.health import health_bp
from routes.items import items_bp
from routes.statistics import statistics_bp
from routes.scrape import scrape_bp
from routes.search import search_bp
from routes.history import history_bp
from routes.websites import website_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(items_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(scrape_bp)
app.register_blueprint(search_bp)
app.register_blueprint(history_bp)
app.register_blueprint(website_bp)

logger = logging.getLogger(__name__)

@app.errorhandler(400)
def bad_request(e):
    logger.warning(f"400 Bad Request: {str(e)}")
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {str(e)}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 Server Error: {str(e)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
