# ⛰️ LandslideWatch — Real-Time Early Warning & Disaster Management System

A production-grade Flask web application for real-time landslide monitoring, 
community incident reporting, and disaster management.

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                           │
│                                                                   │
│  ┌──────────────┐    WiFi     ┌──────────────────────────────┐   │
│  │  ESP8266 MCU │ ──────────► │   Firebase Realtime DB       │   │
│  │  + Sensors   │            │   (LandslideData node)       │   │
│  └──────────────┘            └──────────┬───────────────────┘   │
│                                         │ REST API                │
│  ┌──────────────────────────────────────▼───────────────────┐   │
│  │                  FLASK BACKEND                            │   │
│  │                                                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │   │
│  │  │Dashboard │  │  Map     │  │ Weather  │  │ Report  │  │   │
│  │  │  Route   │  │  Route   │  │  Route   │  │  Route  │  │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘  │   │
│  │       │              │              │              │        │   │
│  │  ┌────▼──────────────▼──────────────▼──────────────▼────┐  │   │
│  │  │                 UTILITIES LAYER                       │  │   │
│  │  │  firebase_client.py | risk_engine.py | weather.py    │  │   │
│  │  └───────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                         │
│              ┌──────────▼──────────┐                             │
│              │  JINJA2 TEMPLATES   │                             │
│              │  + Bootstrap 5 UI   │                             │
│              └──────────┬──────────┘                             │
│                         │                                         │
│         ┌───────────────▼────────────────┐                       │
│         │        EXTERNAL APIs           │                       │
│         │  • OpenWeatherMap (weather)    │                       │
│         │  • OpenRouteService (routes)   │                       │
│         │  • OpenStreetMap (map tiles)   │                       │
│         │  • Leaflet.js (map render)     │                       │
│         └────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
landslide_ews/
├── app.py                    # Flask application factory
├── config.py                 # Configuration (API keys, thresholds)
├── requirements.txt
├── .env.example              # Environment variables template
├── esp8266_firmware.ino      # Arduino sketch for sensor node
│
├── routes/
│   ├── __init__.py
│   ├── dashboard.py          # / — Main sensor dashboard
│   ├── map_view.py           # /map — Live threat map
│   ├── weather.py            # /weather — Weather intelligence
│   ├── report.py             # /report — Incident reporting
│   ├── emergency.py          # /emergency — Emergency help
│   └── api.py                # /api — JSON endpoints for AJAX
│
├── utils/
│   ├── __init__.py
│   ├── firebase_client.py    # Firebase REST client
│   ├── risk_engine.py        # Risk calculation logic
│   └── weather.py            # OpenWeatherMap integration
│
├── templates/
│   ├── base.html             # Base layout (sidebar, topbar)
│   ├── dashboard.html        # Mission control dashboard
│   ├── map.html              # Leaflet + OpenStreetMap
│   ├── weather.html          # Weather forecast page
│   ├── report.html           # Incident report form
│   └── emergency.html        # Emergency contacts & guide
│
└── static/
    ├── css/                  # Custom CSS (if needed)
    ├── js/                   # Custom JavaScript (if needed)
    └── images/               # Logos, icons
```

---

## 🚀 Setup & Running

### 1. Clone & Install
```bash
git clone <repo>
cd landslide_ews
pip install -r requirements.txt
```

### 2. Configure Keys
```bash
cp .env.example .env
# Edit .env with your API keys
```

**Free API Keys needed:**
- **Firebase** → https://console.firebase.google.com (free Spark plan)
- **OpenWeatherMap** → https://openweathermap.org/api (free 1000 calls/day)
- **OpenRouteService** → https://openrouteservice.org (free 2000 req/day)

### 3. Firebase Rules (Development)
```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

### 4. Run
```bash
python app.py
# Visit http://localhost:5000
```

### 5. Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## 🎯 Features

| Feature | Status | Tech |
|---------|--------|------|
| Real-time sensor dashboard | ✅ | Firebase REST + AJAX |
| Risk level computation | ✅ | Custom engine |
| Color-coded risk UI | ✅ | CSS animations |
| Auto-refresh (5s) | ✅ | JavaScript polling |
| Live map with GPS | ✅ | Leaflet + OpenStreetMap |
| Risk zone circle | ✅ | Leaflet.circle |
| Evacuation routes | ✅ | OpenRouteService |
| User location tracking | ✅ | Leaflet.locate |
| Weather integration | ✅ | OpenWeatherMap |
| 5-day forecast | ✅ | OWM Forecast API |
| Intelligent rain alerts | ✅ | Custom logic |
| Community incident reports | ✅ | Firebase + Leaflet |
| Emergency contacts | ✅ | Static + map |
| Mobile responsive | ✅ | Bootstrap 5 |

---

## 🔌 Hardware (ESP8266 Wiring)

| Sensor | Pin | Notes |
|--------|-----|-------|
| Soil Moisture | A0 | Analog read |
| Rain Sensor | D5 | Digital, active LOW |
| Vibration | D6 | Digital |
| DHT11 | D7 | Data pin |
| MPU6050 | SDA/SCL | I2C (D2/D1) |
| GPS (NEO-6M) | D3 (RX) | SoftwareSerial |

---

## 📊 Risk Score Algorithm

```
Score = 0
├── Soil ≥ 70%  → +3 | Soil ≥ 50%  → +1
├── Tilt ≥ 15°  → +3 | Tilt ≥ 8°   → +1
├── Vibration = 1     → +2
└── Rain = 1          → +1

Score 0-1 → SAFE  (green)
Score 2-4 → WARNING (orange)  
Score 5+  → HIGH RISK (red flashing)
```

---

## 👨‍💻 Built For
**Final Year Major Project — Computer Science / Electronics Engineering**
*Real-Time IoT + Web Application for Disaster Management*
# Landslide_EWS
