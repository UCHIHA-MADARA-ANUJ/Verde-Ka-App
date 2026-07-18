# 07. Database Design & JSON Schema

Since **Firebase Realtime Database** is selected as our core synchronizer, the database is designed as a single, highly optimized, real-time JSON Document Tree under the `/Garden` namespace.

---

## 🌳 1. Core Document Tree Schema

```json
{
  "Garden": {
    "Moisture": 52,
    "Temperature": 24.5,
    "Humidity": 65,
    "Light": "Dark",
    "TankLevel": 85,
    "Mode": "MANUAL",
    "Pump": "OFF",
    "LED": "OFF",
    "Threshold": 40,
    "WeatherOverride": 0,
    "Capture": false,
    "TankThreshold": 20,
    "TankWarning": false
  }
}
```

---

## 📝 2. Field-by-Field Definition

### A. Garden Telemetry Nodes
* **`Moisture` (Integer):** 0 to 100, representing real-time soil moisture percentage from the power-gated sensor.
* **`Temperature` (Float):** Ambient temperature in °C from the DHT22/11.
* **`Humidity` (Integer):** Ambient air humidity in % from the DHT22/11.
* **`Light` (String):** "Dark" or "Bright" representing ambient LDR sensor state.
* **`TankLevel` (Integer):** 0 to 100, representing remaining water volume in the bucket from the HC-SR04 ultrasonic sensor.

### B. Garden Control Nodes
* **`Mode` (String):** "MANUAL" or "AUTO". If "MANUAL", ESP32 bypasses local automated loops and obeys app toggles. If "AUTO", ESP32 runs autonomous botanical code.
* **`Pump` (String):** "ON" or "OFF". Controls Relay Channel 1.
* **`LED` (String):** "ON" or "OFF". State of the 5mm UV LED (GPIO 12).
* **`Threshold` (Integer):** User-defined soil target (0-100%) to trigger the water pump in auto-mode.
* **`WeatherOverride` (Integer):** If `1`, local rain predicted; irrigation is suspended. If `0`, active.
* **`Capture` (Boolean):** The trigger flag for the ESP32-CAM.
* **`TankThreshold` (Integer):** User-defined safety target (0-100%) to trigger water level alerts on the dashboard.
* **`TankWarning` (Boolean):** Flag written by Next.js if `TankLevel < TankThreshold`.
