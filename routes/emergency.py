from flask import Blueprint, render_template

emergency_bp = Blueprint("emergency", __name__)

EMERGENCY_CONTACTS = [
    {"name": "National Disaster Management Authority",  "number": "1078", "type": "National"},
    {"name": "Police Emergency",                        "number": "100",  "type": "National"},
    {"name": "Ambulance",                               "number": "108",  "type": "National"},
    {"name": "Fire & Rescue",                           "number": "101",  "type": "National"},
    {"name": "Kerala Disaster Management Authority",    "number": "1070", "type": "State"},
    {"name": "District Collector (Kozhikode)",         "number": "0495-2371372", "type": "Local"},
]

@emergency_bp.route("/")
def emergency_view():
    return render_template("emergency.html", contacts=EMERGENCY_CONTACTS)
