from flask import Blueprint, render_template
from utils.firebase_client import get_sensor_data, get_reports
from utils.risk_engine import compute_risk

map_bp = Blueprint("map_view", __name__)

@map_bp.route("/")
def map_view():
    data    = get_sensor_data()
    risk    = compute_risk(data)
    reports = get_reports()
    lat     = float(data.get("Latitude") or 11.2588)
    lon     = float(data.get("Longitude") or 75.7804)
    return render_template("map.html", data=data, risk=risk,
                           reports=reports, lat=lat, lon=lon)
