# 13. System Notifications & Alarms

This document outlines the system-level alarm configurations and notification flows designed for **Project Verde V3.0**.

---

## 🚨 1. Critical Alarm Flows

### A. Water Reservoir Empty (Dry Run Prevention)
* **Trigger:** The HC-SR04 ultrasonic sensor reads water depth $<10\%$ in the bucket.
* **App Action:**
  1. The app dashboard immediately rings a warning buzzer.
  2. The water bucket cylinder gauge turns bright, flashing red.
  3. Displays a persistent modal warning: *"🚨 CRITICAL: Water Reservoir Empty! Pump has been deactivated to prevent motor burnout. Please fill bucket manually."*
* **Hardware Action:** The ESP32 software automatically overrides all irrigation commands, pulling **PUMP_RELAY HIGH (OFF)** instantly, saving your pump from burning out!

### B. Smart Weather Irrigation Suspension
* **Trigger:** Next.js cron syncs with OpenWeatherMap and detects Delhi rain.
* **App Action:**
  1. Renders a pulsing green cloud banner on top of the dashboard.
  2. Displays: *"⛈️ Weather Sync: Rain predicted in Delhi. Automated watering suspended to conserve resources."*
* **Hardware Action:** ESP32 reads `weather_override = 1` and blocks the water pump from turning on, even if the soil is dry!

---

## 🔔 2. In-App Toast Alerts
* **Low Light Warning:** When LDR reads $<400$ LUX, slide in a brief green toast: *"☀️ Grow Light Activated: Direct 5mm UV LED turned ON."*
* **Watering Success:** When soil moisture increases by 5% after irrigation, show a success toast: *"💧 Irrigation Complete: Plant successfully watered."*
