import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS
from routes.health import health_bp
from routes.items import items_bp
from routes.statistics import statistics_bp
from routes.scrape import scrape_bp
from routes.search import search_bp
from routes.history import history_bp
from routes.websites import website_bp
from services.scheduler import init_scheduler, shutdown_scheduler
import atexit
from routes.display import display_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(items_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(scrape_bp)
app.register_blueprint(search_bp)
app.register_blueprint(history_bp)
app.register_blueprint(display_bp)
app.register_blueprint(website_bp)

logger = logging.getLogger(__name__)

# Background scraping (opt-in). See services/scheduler.py for the
# SCRAPE_SCHEDULER_ENABLED / SCRAPE_INTERVAL_MINUTES env vars.
init_scheduler(app)
atexit.register(shutdown_scheduler)

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
    # Debug mode (and the interactive Werkzeug debugger it enables) must never
    # be hardcoded on, since it allows arbitrary code execution if an
    # unhandled exception occurs. It now defaults to off and can only be
    # turned on explicitly via an environment variable for local development.
    debug_mode = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode)
