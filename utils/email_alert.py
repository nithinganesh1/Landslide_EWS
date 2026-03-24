import smtplib
from email.mime.text import MIMEText
from config import Config

SMTP_SERVER = Config.SMTP_SERVER
SMTP_PORT = Config.SMTP_PORT


def send_alert_email(vibration, soil):
    """Send alert email for vibration or high soil moisture."""
    
    email_sender = Config.EMAIL_SENDER
    app_password = Config.EMAIL_APP_PASSWORD
    recipients = Config.EMAIL_RECIPIENTS
    soil_threshold = Config.RISK_HIGH_SOIL
    
    if not app_password:
        print("ERROR: EMAIL_APP_PASSWORD not set")
        return
    
    # Determine alert type and vibration message
    if vibration == 1:
        subject = "⚠ CRITICAL: Vibration Detected - Landslide Alert"
        alert_type = "VIBRATION DETECTED"
        vibration_msg = "Vibration is VERY HIGH"
    elif soil > soil_threshold:
        subject = "⚠ WARNING: High Soil Moisture - Landslide Risk"
        alert_type = "HIGH SOIL MOISTURE"
        vibration_msg = "Vibration: Normal"
    else:
        subject = "⚠ Landslide Warning Detected"
        alert_type = "SENSOR ALERT"
        vibration_msg = "Vibration: Normal"
    
    body = f"""
Landslide Early Warning System Alert

Alert Type    : {alert_type}
Soil Moisture : {soil}% (Threshold: {soil_threshold}%)
{vibration_msg}

Please take precautions immediately.
"""
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_sender
    msg["To"] = ", ".join([r.strip() for r in recipients])
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(email_sender, app_password)
        
        # Send to all recipients
        server.sendmail(email_sender, recipients, msg.as_string())
        server.quit()
        
        print(f"✓ Email alert sent ({alert_type}) to {len(recipients)} recipients")
        
    except Exception as e:
        print(f"✗ Email error: {e}")