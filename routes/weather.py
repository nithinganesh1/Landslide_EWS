from flask import Blueprint, render_template
from utils.firebase_client import get_sensor_data
from utils.weather import get_current_weather, get_forecast, get_alerts_message

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/")
def weather_view():
    data = get_sensor_data()
    lat  = float(data.get("Latitude") or 11.2588)
    lon  = float(data.get("Longitude") or 75.7804)
    current  = get_current_weather(lat, lon)
    forecast = get_forecast(lat, lon)
    alert    = get_alerts_message(lat, lon)
    return render_template("weather.html", current=current,
                           forecast=forecast, alert=alert, lat=lat, lon=lon)
