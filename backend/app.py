from flask import Flask
from flask_cors import CORS
from routes.health import health_bp
from routes.items import items_bp
from routes.statistics import statistics_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(items_bp)
app.register_blueprint(statistics_bp)

if __name__ == '__main__':
    app.run(debug=True)
