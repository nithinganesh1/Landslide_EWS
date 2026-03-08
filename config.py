import os

class Config:
    # ── Firebase — matches ESP8266 firmware exactly ───────────
    FIREBASE_URL = os.getenv(
        "FIREBASE_URL",
        "https://landslide-ews-6b9d0-default-rtdb.firebaseio.com"  # your real project
    )
    FIREBASE_API_KEY = os.getenv(
        "FIREBASE_API_KEY",
        "AIzaSyDUP2UOyFX6boBzM5wOsRJPant_wrD0eig"  # your real API key
    )

    # ── Weather ───────────────────────────────────────────────
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OWM_KEY")
    OPENWEATHER_BASE    = "https://api.openweathermap.org/data/2.5"

    # ── Routing ───────────────────────────────────────────────
    ORS_API_KEY  = os.getenv("ORS_API_KEY", "YOUR_ORS_KEY")
    ORS_BASE_URL = "https://api.openrouteservice.org/v2"

    # ── Risk Thresholds ───────────────────────────────────────
    RISK_HIGH_SOIL = 70
    RISK_HIGH_TILT = 15
    RISK_WARN_SOIL = 50
    RISK_WARN_TILT = 8
