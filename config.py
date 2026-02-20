# =============================================================
# CONFIGURATION — Landslide Early Warning System
# =============================================================
import os

class Config:
    # ── Firebase ──────────────────────────────────────────────
    FIREBASE_URL = os.getenv(
        "FIREBASE_URL",
        "https://your-project-default-rtdb.firebaseio.com"
    )
    FIREBASE_API_KEY        = os.getenv("FIREBASE_API_KEY", "YOUR_FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN    = os.getenv("FIREBASE_AUTH_DOMAIN", "your-project.firebaseapp.com")
    FIREBASE_PROJECT_ID     = os.getenv("FIREBASE_PROJECT_ID", "your-project-id")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "your-project.appspot.com")
    FIREBASE_MESSAGING_ID   = os.getenv("FIREBASE_MESSAGING_ID", "123456789")
    FIREBASE_APP_ID         = os.getenv("FIREBASE_APP_ID", "1:123:web:abc")

    # ── Weather ───────────────────────────────────────────────
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OWM_KEY")
    OPENWEATHER_BASE    = "https://api.openweathermap.org/data/2.5"

    # ── Routing ───────────────────────────────────────────────
    ORS_API_KEY  = os.getenv("ORS_API_KEY", "YOUR_ORS_KEY")
    ORS_BASE_URL = "https://api.openrouteservice.org/v2"

    # ── Risk Thresholds ───────────────────────────────────────
    RISK_HIGH_SOIL      = 70   # %
    RISK_HIGH_TILT      = 15   # degrees
    RISK_HIGH_VIBRATION = 1
    RISK_HIGH_RAIN      = 1

    RISK_WARN_SOIL      = 50
    RISK_WARN_TILT      = 8
