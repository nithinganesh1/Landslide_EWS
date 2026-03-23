import smtplib
from email.mime.text import MIMEText

# sender gmail
EMAIL = "joelproject72@gmail.com"
APP_PASSWORD = "hyyj zgaz pvjn jvqu"

# receiver email (where alert should go)
RECEIVER_EMAIL = "yourdestination@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_alert_email(vibration, soil):

    subject = "⚠ Landslide Warning Detected"

    body = f"""
Landslide Early Warning System Alert

Danger detected.

Soil Moisture : {soil}
Vibration     : {vibration}

Please take precautions immediately.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)

        server.sendmail(EMAIL, RECEIVER_EMAIL, msg.as_string())

        server.quit()

        print("Email alert sent")

    except Exception as e:
        print("Email error:", e)