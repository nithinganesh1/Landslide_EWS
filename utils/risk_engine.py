"""
utils/risk_engine.py
Computes risk level + human-readable reason from sensor data.

Sensor polarity notes (from ESP8266 firmware):
  Rain sensor    → active LOW: digitalRead 0 = rain, 1 = no rain
  Vibration      → active HIGH: digitalRead 1 = vibration detected
  Tilt (MPU6050) → abs(acceleration.x) in m/s², threshold ~8
"""
from config import Config

def compute_risk(data: dict) -> dict:
    soil      = float(data.get("SoilMoisture", 0))
    tilt      = float(data.get("Tilt", 0))
    vibration = int(data.get("Vibration", 0))   # 1 = detected (active HIGH)

    # Rain sensor is active-LOW on the ESP8266:
    #   Firebase receives 0 (LOW)  → rain IS falling
    #   Firebase receives 1 (HIGH) → no rain
    # We invert so rain=1 means "raining" throughout the rest of the code.
    rain_raw = int(data.get("Rain", 1))
    rain = 1 if rain_raw == 0 else 0

    reasons = []
    score   = 0

    if soil >= Config.RISK_HIGH_SOIL:
        score += 3; reasons.append(f"Critical soil saturation ({soil:.0f}%)")
    elif soil >= Config.RISK_WARN_SOIL:
        score += 1; reasons.append(f"Elevated soil moisture ({soil:.0f}%)")

    if tilt >= Config.RISK_HIGH_TILT:
        score += 3; reasons.append(f"Dangerous ground tilt ({tilt:.1f} m/s²)")
    elif tilt >= Config.RISK_WARN_TILT:
        score += 1; reasons.append(f"Moderate tilt detected ({tilt:.1f} m/s²)")

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
        "level":     level,
        "score":     score,
        "reasons":   reasons or ["All parameters within safe limits"],
        "color":     {"SAFE": "#15803d", "WARNING": "#b45309", "HIGH RISK": "#b91c1c"}[level],
        "css_class": {"SAFE": "safe",    "WARNING": "warning",  "HIGH RISK": "danger"}[level],
        # Raw parsed values — useful for the dashboard JS
        "parsed": {
            "soil": soil, "tilt": tilt,
            "vibration": vibration, "rain": rain,
        }
    }
