from flask import Blueprint, render_template
from utils.firebase_client import get_sensor_data

emergency_bp = Blueprint("emergency", __name__)

EMERGENCY_CONTACTS = [
    # National
    {"name": "National Disaster Management Authority",  "number": "1078", "type": "National"},
    {"name": "National Emergency Number",              "number": "112",  "type": "National"},
    {"name": "Ambulance",                               "number": "108",  "type": "National"},
    {"name": "Police Emergency",                        "number": "100",  "type": "National"},
    {"name": "Fire & Rescue",                           "number": "101",  "type": "National"},
    # State/District
    {"name": "Kerala Disaster Management Authority",    "number": "1070", "type": "State"},
    {"name": "Ernakulam District Collector",            "number": "0484-2350911", "type": "District"},
    {"name": "Aluva Police Station",                    "number": "0484-2624100", "type": "Local"},
    {"name": "Aluva Fire Station",                      "number": "0484-2629999", "type": "Local"},
    {"name": "Aluva Municipal Corporation",             "number": "0484-2621122", "type": "Local"},
]

@emergency_bp.route("/")
def emergency_view():
    data = get_sensor_data()
    lat = float(data.get("Latitude") or 9.9774)  # Aluva coordinates
    lon = float(data.get("Longitude") or 76.3427)
    return render_template("emergency.html", contacts=EMERGENCY_CONTACTS, lat=lat, lon=lon)
