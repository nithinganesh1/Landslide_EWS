from flask import Blueprint, render_template
from utils.firebase_client import get_sensor_data
from utils.risk_engine import compute_risk
from utils.weather import get_current_weather, get_alerts_message

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    data   = get_sensor_data()
    risk   = compute_risk(data)
    lat    = float(data.get("Latitude") or 11.2588)
    lon    = float(data.get("Longitude") or 75.7804)
    weather = get_current_weather(lat, lon)
    alert_msg = get_alerts_message(lat, lon)
    return render_template(
        "dashboard.html",
        data=data,
        risk=risk,
        weather=weather,
        alert_msg=alert_msg,
        lat=lat,
        lon=lon,
    )
