from flask import Flask
from routes.dashboard import dashboard_bp
from routes.map_view import map_bp
from routes.weather import weather_bp
from routes.report import report_bp
from routes.emergency import emergency_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "landslide_ews_secret_2024"

    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(map_bp, url_prefix="/map")
    app.register_blueprint(weather_bp, url_prefix="/weather")
    app.register_blueprint(report_bp, url_prefix="/report")
    app.register_blueprint(emergency_bp, url_prefix="/emergency")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
