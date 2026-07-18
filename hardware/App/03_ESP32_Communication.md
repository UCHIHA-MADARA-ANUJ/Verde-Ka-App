# 03. ESP32 Communication Protocol

This document details the telemetry, controls, and Wi-Fi reconnection architectures of the **ESP32 DevKit V1** main controller under the `/Garden` path.

---

## 📡 1. Communication Protocols & Transport
All communication between the main controller and the cloud is handled over bidirectionally streamed WebSockets using the **`FirebaseESP32`** library. This completely bypasses slow HTTP REST polling and allows instant, sub-second manual triggers.

---

## 💾 2. Payload Schema Specifications

### A. /Garden Node (Telemetry Output)
Published to the `/Garden` path of your Firebase RTDB every **1 second**:

* **JSON Schema:**
```json
{
  "Moisture": 52,
  "Temperature": 24.5,
  "Humidity": 65,
  "Light": "Dark",
  "TankLevel": 85
}
```

* **Data Field Validation (Strict Constraints):**
  * `Moisture`: Integer, constrained between `0` (bone dry) and `100` (completely saturated).
  * `Temperature`: Float, scaled to 1 decimal place.
  * `Humidity`: Integer, ambient humidity %.
  * `Light`: String, "Dark" or "Bright" indicating ambient light levels.
  * `TankLevel`: Integer, constrained between `0` (water bucket empty) and `100` (water bucket full), calculated from HC-SR04 ultrasonic distance measurements.

### B. Garden Control Fields (State Input/Output)
Read by the ESP32 continuously over an open WebSocket stream:

* **JSON Schema:**
```json
{
  "Mode": "MANUAL",
  "Pump": "OFF",
  "LED": "OFF",
  "Threshold": 40,
  "WeatherOverride": 0
}
```

* **Data Field Definitions:**
  * `Mode`: String, "MANUAL" or "AUTO". If "MANUAL", ESP32 bypasses local automated loops and relies strictly on user toggles. If "AUTO", ESP32 runs autonomous botanical code.
  * `Pump`: String, "ON" or "OFF". Controls Relay Channel 1 (GPIO 5).
  * `LED`: String, "ON" or "OFF". Controls the direct 5mm UV LED pin (GPIO 12).
  * `Threshold`: Integer (0-100), sets the target soil moisture level.
  * `WeatherOverride`: Integer. If `1`, rain is predicted locally; ESP32 suspends irrigation. If `0`, irrigation is active.

---

## ⚡ 3. Non-Blocking Wi-Fi Reconnection Architecture

During exhibitions, Wi-Fi hotspots can drop under high network congestion. Standard `while(WiFi.status() != WL_CONNECTED)` code will freeze the ESP32, blocking your local irrigation safety loops. 

To prevent this, the ESP32 must run a **non-blocking, timer-based reconnection routine** using `millis()`:

```cpp
unsigned long lastWiFiCheck = 0;
const unsigned long wifiRetryInterval = 5000; // Check and retry every 5 seconds

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    unsigned long currentMillis = millis();
    if (currentMillis - lastWiFiCheck > wifiRetryInterval) {
      lastWiFiCheck = currentMillis;
      Serial.println("Wi-Fi Connection lost! Retrying in background...");
      WiFi.disconnect();
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD); // Non-blocking reconnection request
    }
  }
}
```
* **Why this is critical:** Even if your Wi-Fi hotspot goes offline for hours, the ESP32 will continue running its main loop, checking local moisture levels, and controlling the pump locally, ensuring plant survival!
