from utils.firebase_client import get_sensor_data
from utils.email_alert import send_alert_email

SOIL_THRESHOLD = 70


def check_alert():

    data = get_sensor_data()

    soil = float(data.get("SoilMoisture", 0))
    vibration = int(data.get("Vibration", 0))

    print("Soil:", soil, "Vibration:", vibration)

    if soil > SOIL_THRESHOLD and vibration == 1:
        print("ALERT CONDITION TRUE")
        send_alert_email(vibration, soil)
    else:
        print("No danger condition")
