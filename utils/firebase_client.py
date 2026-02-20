"""
utils/firebase_client.py
Reads from / writes to Firebase Realtime Database using the REST API
(no service-account file needed for public/open rules).
"""
import requests
import time
from config import Config

BASE = Config.FIREBASE_URL.rstrip("/")


def get_sensor_data() -> dict:
    """Return latest LandslideData node."""
    try:
        r = requests.get(f"{BASE}/LandslideData.json", timeout=5)
        r.raise_for_status()
        data = r.json() or {}
        return data
    except Exception as e:
        return _mock_data()


def push_report(report: dict) -> bool:
    """Append a user report to UserReports node."""
    try:
        report["timestamp"] = int(time.time())
        r = requests.post(f"{BASE}/UserReports.json", json=report, timeout=5)
        r.raise_for_status()
        return True
    except Exception:
        return False


def get_reports() -> list:
    """Fetch all user reports as a list."""
    try:
        r = requests.get(f"{BASE}/UserReports.json", timeout=5)
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        return [{"id": k, **v} for k, v in data.items()]
    except Exception:
        return []


def _mock_data() -> dict:
    """Fallback demo data when Firebase is unreachable."""
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
