from flask import Blueprint, jsonify
from utils.firebase_client import get_sensor_data, get_reports
from utils.risk_engine import compute_risk
from utils.weather import get_current_weather, get_alerts_message

api_bp = Blueprint("api", __name__)

@api_bp.route("/sensor")
def sensor():
    data = get_sensor_data()
    risk = compute_risk(data)
    return jsonify({"sensor": data, "risk": risk})

@api_bp.route("/weather")
def weather():
    data = get_sensor_data()
    lat  = float(data.get("Latitude") or 11.2588)
    lon  = float(data.get("Longitude") or 75.7804)
    w    = get_current_weather(lat, lon)
    alert = get_alerts_message(lat, lon)
    return jsonify({"weather": w, "alert": alert})

@api_bp.route("/reports")
def reports():
    return jsonify(get_reports())
