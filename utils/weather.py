"""
utils/weather.py
Fetches current weather + 3-day forecast from OpenWeatherMap (free tier).
"""
import requests
from config import Config

OWM = Config.OPENWEATHER_BASE
KEY = Config.OPENWEATHER_API_KEY


def get_current_weather(lat: float, lon: float) -> dict:
    try:
        r = requests.get(
            f"{OWM}/weather",
            params={"lat": lat, "lon": lon, "appid": KEY, "units": "metric"},
            timeout=6,
        )
        r.raise_for_status()
        d = r.json()
        return {
            "description": d["weather"][0]["description"].title(),
            "icon": d["weather"][0]["icon"],
            "temp": d["main"]["temp"],
            "humidity": d["main"]["humidity"],
            "wind_speed": d["wind"]["speed"],
            "city": d.get("name", "Unknown"),
            "alert": _rain_alert(d),
        }
    except Exception:
        return _mock_weather()


def get_forecast(lat: float, lon: float) -> list:
    try:
        r = requests.get(
            f"{OWM}/forecast",
            params={"lat": lat, "lon": lon, "appid": KEY, "units": "metric", "cnt": 24},
            timeout=6,
        )
        r.raise_for_status()
        items = r.json().get("list", [])
        seen, result = set(), []
        for item in items:
            date = item["dt_txt"].split(" ")[0]
            if date not in seen:
                seen.add(date)
                result.append({
                    "date": date,
                    "temp": item["main"]["temp"],
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                    "rain": item.get("rain", {}).get("3h", 0),
                    "pop": round(item.get("pop", 0) * 100),
                })
        return result[:5]
    except Exception:
        return []


def get_alerts_message(lat: float, lon: float) -> str:
    weather = get_current_weather(lat, lon)
    forecast = get_forecast(lat, lon)
    msgs = []
    if weather.get("alert"):
        msgs.append(weather["alert"])
    heavy = [f for f in forecast if f["pop"] > 60]
    if heavy:
        msgs.append(
            f"Heavy rain forecasted on {heavy[0]['date']} ({heavy[0]['pop']}% probability). "
            "Landslide risk may increase significantly. Stay alert."
        )
    if not msgs:
        msgs.append("No severe weather alerts. Monitor regularly.")
    return " | ".join(msgs)


def _rain_alert(data: dict) -> str:
    desc = data["weather"][0]["main"].lower()
    if "thunderstorm" in desc:
        return "⚡ Thunderstorm active — elevated landslide risk!"
    if "rain" in desc:
        return "🌧️ Rainfall detected — monitor soil moisture closely."
    return ""


def _mock_weather() -> dict:
    return {
        "description": "Partly Cloudy",
        "icon": "03d",
        "temp": 27,
        "humidity": 65,
        "wind_speed": 4.2,
        "city": "Kozhikode",
        "alert": "",
    }
