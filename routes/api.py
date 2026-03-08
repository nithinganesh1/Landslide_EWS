from flask import Blueprint, jsonify, request
from utils.firebase_client import get_sensor_data, get_reports, BASE, _CONFIGURED
from utils.risk_engine import compute_risk
from utils.weather import get_current_weather, get_alerts_message
import requests, time, math

api_bp = Blueprint("api", __name__)

# Hospitals database - Aluva area + nearby
HOSPITALS_DB = [
    # Aluva
    {"name": "Aluva Shanthigiri Medical Centre", "loc": "Aluva", "number": "0484-2620222", "lat": 9.9774, "lon": 76.3427},
    {"name": "Dr. Mohan's Hospital Aluva", "loc": "Aluva", "number": "0484-2624466", "lat": 9.9780, "lon": 76.3450},
    {"name": "Aluva Medical Clinic", "loc": "Aluva", "number": "0484-2622333", "lat": 9.9750, "lon": 76.3400},
    # Nearby areas
    {"name": "Ernakulam Medical Centre", "loc": "Ernakulam", "number": "0484-2395555", "lat": 9.9815, "lon": 76.2900},
    {"name": "Lourdes Hospital Kochi", "loc": "Kochi", "number": "0484-2206666", "lat": 9.9689, "lon": 76.2675},
]

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371  # Earth's radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

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

@api_bp.route("/hospitals")
def hospitals():
    """Get nearest hospitals from Aluva database"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({"error": "lat and lon parameters required"}), 400
    
    # Calculate distances and sort
    hospitals_with_distance = [
        {
            **h,
            "distance": round(haversine_distance(lat, lon, h['lat'], h['lon']), 1)
        }
        for h in HOSPITALS_DB
    ]
    hospitals_with_distance.sort(key=lambda x: x['distance'])
    
    return jsonify(hospitals_with_distance)

@api_bp.route("/reports")
def reports():
    return jsonify(get_reports())

@api_bp.route("/debug")
def debug():
    """
    Diagnostic endpoint — visit /api/debug in browser to see
    exactly why Firebase writes are failing.
    """
    info = {
        "firebase_url":   BASE,
        "url_configured": _CONFIGURED,
        "timestamp":      int(time.time()),
    }

    if not _CONFIGURED:
        info["error"] = "FIREBASE_URL is not in the .env file or is invalid."
        return jsonify(info), 500

    # Test read
    try:
        r = requests.get(f"{BASE}/LandslideData.json", timeout=5)
        info["read_status"]   = r.status_code
        info["read_ok"]       = r.ok
        info["read_response"] = r.json() if r.ok else r.text[:300]
    except Exception as e:
        info["read_error"] = str(e)

    # Test write
    test_payload = {"_test": True, "ts": int(time.time())}
    try:
        w = requests.post(f"{BASE}/UserReports.json", json=test_payload, timeout=5)
        info["write_status"]   = w.status_code
        info["write_ok"]       = w.ok
        info["write_response"] = w.json() if w.ok else w.text[:300]
        # Clean up the test entry
        if w.ok:
            key = w.json().get("name")
            if key:
                requests.delete(f"{BASE}/UserReports/{key}.json", timeout=3)
    except Exception as e:
        info["write_error"] = str(e)

    status_code = 200 if info.get("write_ok") else 500
    return jsonify(info), status_code
