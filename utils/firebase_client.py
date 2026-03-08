"""
utils/firebase_client.py
Reads from / writes to Firebase Realtime Database using REST API.
Matches the ESP8266 Firebase setup: test_mode=true, API key auth.
"""
import requests
import time
import logging
from config import Config

log = logging.getLogger(__name__)

# Build the base URL — handle with or without https://
_raw = Config.FIREBASE_URL.strip()
if not _raw.startswith("http"):
    _raw = "https://" + _raw
BASE = _raw.rstrip("/")

API_KEY = Config.FIREBASE_API_KEY   # appended as ?auth= for REST writes

_CONFIGURED = "your-project" not in BASE and BASE != "https://"


def _auth_params():
    """Return query params dict with auth key if configured."""
    if API_KEY and API_KEY != "YOUR_FIREBASE_API_KEY":
        return {"auth": API_KEY}
    return {}


def get_sensor_data() -> dict:
    try:
        r = requests.get(
            f"{BASE}/LandslideData.json",
            params=_auth_params(),
            timeout=5,
        )
        r.raise_for_status()
        return r.json() or {}
    except Exception as e:
        log.warning("get_sensor_data failed: %s — using mock data", e)
        return _mock_data()


def push_report(report: dict) -> tuple[bool, str]:
    """
    Write a new report under /UserReports using POST (auto push-key).
    Returns (success: bool, error_message: str).
    """
    if not _CONFIGURED:
        msg = (
            "Firebase URL is not configured. "
            f"Current value: '{BASE}'. "
            "Set FIREBASE_URL=https://landslide-ews-6b9d0-default-rtdb.firebaseio.com "
            "in your .env file."
        )
        log.error(msg)
        return False, msg

    report["timestamp"] = int(time.time())
    url = f"{BASE}/UserReports.json"

    try:
        r = requests.post(url, json=report, params=_auth_params(), timeout=8)
    except requests.exceptions.ConnectionError as e:
        msg = f"Cannot reach Firebase — check internet connection. ({e})"
        log.error("push_report ConnectionError: %s", e)
        return False, msg
    except requests.exceptions.Timeout:
        msg = "Firebase request timed out. Please try again."
        log.error("push_report Timeout: %s", url)
        return False, msg

    if r.status_code in (401, 403):
        msg = (
            f"Firebase rejected the write (HTTP {r.status_code}). "
            "Go to Firebase Console → Realtime Database → Rules and set: "
            '{ "rules": { ".read": true, ".write": true } }'
        )
        log.error("push_report auth error %s: %s", r.status_code, r.text)
        return False, msg

    if not r.ok:
        msg = f"Firebase error HTTP {r.status_code}: {r.text[:300]}"
        log.error("push_report failed: %s", msg)
        return False, msg

    log.info("push_report OK → %s", r.json())
    return True, ""


def get_reports() -> list:
    try:
        r = requests.get(
            f"{BASE}/UserReports.json",
            params=_auth_params(),
            timeout=5,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        return [{"id": k, **v} for k, v in data.items()]
    except Exception as e:
        log.warning("get_reports failed: %s", e)
        return []


def _mock_data() -> dict:
    return {
        "Humidity": 62,
        "Latitude": 11.2588,
        "Longitude": 75.7804,
        "Rain": 1,
        "RiskLevel": "WARNING",
        "SoilMoisture": 55,
        "Temperature": 26.7,
        "Tilt": 9,
        "Vibration": 1,
        "Timestamp": int(time.time()),
    }
