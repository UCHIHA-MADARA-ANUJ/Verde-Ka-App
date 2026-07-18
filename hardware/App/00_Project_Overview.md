# 00. Project Overview & Technical Specification

## 🎯 1. Project Goal
The ultimate objective of **Project Verde V3.0 (Autonomous Plant OS)** is to build an industrial-grade, low-cost, smart residential gardening and precision agritech system. It enables remote, automated, and AI-assisted plant care from anywhere in the world. By shifting from a complex co-processing system to a single-brain WROOM-32 platform, the project achieves maximum reliability, stable wireless operations, and an extremely neat, non-messy physical build.

This version is **fully backward-compatible with your previous science exhibition build**, aligning 100% with your existing database paths under the **`/Garden`** namespace (e.g. `/Garden/Moisture`, `/Garden/Mode`, `/Garden/Pump`, `/Garden/LED`).

## 👥 2. Target Users & Expected Audits
* **Residential Gardeners:** Individuals who travel frequently and require a set-and-forget remote irrigation system.
* **DAV ACON 5 Tech Exhibition Judges:** Evaluators requiring extreme scientific rigor, stable electronics design, zero-error software-hardware integration, and a neat, high-performance physical prototype.
* **Agritech Researchers:** Hobbyists looking to bench-test plant growth behaviors under full-spectrum artificial LED grow lights and precise moisture targets.

## ⚙️ 3. Key System Components & Tech Stack
The physical and digital layers of Verde Tech V3.0 are completely decoupled to prevent single-point failures:

### A. The Master Brain: ESP32 DevKit V1 (30-Pin, CP2102, Type-C)
* **Role:** The central data aggregator and actuator. It handles the local control loop, communicates with sensors, and streams variables over WiFi to the cloud.
* **Breakout Shield:** Techtonics 30-Pin Breakout Expansion Board. Sits under the ESP32 and breaks out all pins into Ground-VCC-Signal (G-V-S) header sets. **This completely eliminates loose breadboard wiring clutter!**
* **DHT22/DHT11 Sensor (Ambient Temp/Hum):** Measures ambient parameters with decimal precision (connected to GPIO 4).
* **2-Prong Moisture Sensor:** Measures volumetric water content in the soil (AO to GPIO 34, gated VCC to GPIO 23 to prevent corrosion).
* **HC-SR04 Ultrasonic Sensor:** Measures water level inside the bucket reservoir (TRIG to GPIO 18, ECHO to GPIO 19).
* **LDR Light Sensor:** Detects ambient light levels to determine grow light state (GPIO 14).
* **5V Submersible Pump:** Low-power 5V pump that can lift water up to 1 meter (Relay 1 connected to GPIO 5).
* **Everlight 5mm UV LED:** Low-power ultraviolet light emitting diode used as a local photosynthetic grow light (directly driven via GPIO 12 with a 220-Ohm series resistor).

### B. The Standalone Vision Node: ESP32-CAM (AI-Thinker, OV2640, MB Shield)
* **Role:** An independent wireless camera. It remains in a low-power idle state and captures a high-resolution snapshot *only on user request (on appeal)* from the Next.js application.
* **MB USB Programmer Shield:** Snaps onto the back of the camera. Provides a native Micro-USB port for programming and clean 5V power, making the camera completely wireless from the main breadboard.
* **8MHz Clock Configuration:** Throttles the camera's master clock (`XCLK`) to **8MHz** to eliminate any Wi-Fi RF antenna interference.

### C. The Cloud Sync Bridge: Firebase Realtime Database (RTDB)
* **Role:** A WebSocket-level synchronization database that acts as a real-time state machine between the Next.js app and the microcontrollers. It guarantees sub-100ms latency on manual overrides.

### D. The Application Layer: Next.js + Tailwind + Vercel
* **The Web Client:** Built using Next.js (App Router) and Tailwind CSS, hosted on Vercel. Renders live telemetry gauges, historical charts, manual actuator buttons, and the AI chatbot terminal.
* **The Serverless Backend:** Node.js API routes that handle binary image uploads, write files to Firebase Storage, fetch Delhi weather forecasts, and connect to Plant.id and Gemini 2.0 Flash.

---

## 🗺️ 5. Unified System Block Diagram

```
 +-------------------------------------------------------------------------------------------------+
 |                                     PHYSICAL SYSTEM BOUNDARY                                    |
 |                                                                                                 |
 |  [ ESP32-CAM Vision Node ]                           [ ESP32 Main Control Deck ]                |
 |  - Powered via USB-C on MB Shield                    - Powered via USB-C on Expansion Shield    |
 |  - Standalone Wi-Fi Connection                       - Gated 2-Prong Moisture, DHT11/22, LDR    |
 |  - Idle until Firebase trigger                       - Standard 1s Telemetry stream             |
 |                                                                                                 |
 +----------------────────────────┬────────────────────────────────┬────────────────---------------+
                                  │                                │
                             (WiFi Sync)                      (WiFi Sync)
                                  ▼                                ▼
 +-------------------------------------------------------------------------------------------------+
 |                                       CLOUD SYSTEM BOUNDARY                                     |
 |                                                                                                 |
 |                            [ Firebase Realtime Database (RTDB) ]                                |
 |                            - Real-time JSON Tree Synchronization under /Garden                 |
 |                            - Handshakes, Toggles, Thresholds, and Telemetry                     |
 |                                                                                                 |
 +--------------------------------───────────────┬────────────────────────────────────────────────-+
                                                 │
                                            (WebSockets)
                                                 ▼
 +-------------------------------------------------------------------------------------------------+
 |                                      NEXT.JS CLIENT BOUNDARY                                    |
 |                                                                                                 |
 |     [ Vercel Serverless Backend APIs ]             ◄========►       [ Web Dashboard Client ]    |
 |     - /api/upload-photo (Node.js buffer upload)                     - Glowing Cyberpunk UI      |
 |     - /api/analyze-plant (Plant.id + Gemini 2.0)                    - Recharts Telemetry plot   |
 |     - /api/weather-sync (Hourly OpenWeather Sync)                   - Manual/Auto Switch Deck   |
 |                                                                                                 |
 +-------------------------------------------------------------------------------------------------+
```
