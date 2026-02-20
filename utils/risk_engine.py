"""
utils/risk_engine.py
Computes risk level + human-readable reason from sensor data.
"""
from config import Config

def compute_risk(data: dict) -> dict:
    soil      = float(data.get("SoilMoisture", 0))
    tilt      = float(data.get("Tilt", 0))
    vibration = int(data.get("Vibration", 0))
    rain      = int(data.get("Rain", 0))

    reasons = []
    score   = 0

    if soil >= Config.RISK_HIGH_SOIL:
        score += 3; reasons.append(f"Critical soil saturation ({soil:.0f}%)")
    elif soil >= Config.RISK_WARN_SOIL:
        score += 1; reasons.append(f"Elevated soil moisture ({soil:.0f}%)")

    if tilt >= Config.RISK_HIGH_TILT:
        score += 3; reasons.append(f"Dangerous ground tilt ({tilt:.1f}°)")
    elif tilt >= Config.RISK_WARN_TILT:
        score += 1; reasons.append(f"Moderate tilt detected ({tilt:.1f}°)")

    if vibration:
        score += 2; reasons.append("Ground vibration detected")

    if rain:
        score += 1; reasons.append("Active rainfall")

    if score >= 5:
        level = "HIGH RISK"
    elif score >= 2:
        level = "WARNING"
    else:
        level = "SAFE"

    return {
        "level": level,
        "score": score,
        "reasons": reasons or ["All parameters within safe limits"],
        "color": {"SAFE": "#22c55e", "WARNING": "#f59e0b", "HIGH RISK": "#ef4444"}[level],
        "css_class": {"SAFE": "safe", "WARNING": "warning", "HIGH RISK": "danger"}[level],
    }
