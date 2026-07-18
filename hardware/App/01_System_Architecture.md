# 01. System Architecture & Component Specifications

This document contains the un-truncated, detailed specifications of every hardware module and software service deployed in **Project Verde V3.0**.

---

## 🛠️ 1. Edge Layer Hardware Specifications

```
             +───────────────────────────────────────────+
             |         ESP32 WROOM-32 Controller         |
             +───────────────────────────────────────────+
                                   │
                     +─────────────┴─────────────+
                     ▼                           ▼
                   [ ESP32 Breakout Shield ]  [ Half-Size Breadboard ]
                     │                           │
       +─────────────┼─────────────+             ├─► 1000uF Capacitor (Power)
       ▼             ▼             ▼             ├─► 1N4007 Diode (Pump back-EMF)
    [Sensors]    [Actuators]  [Breakout]         └─► 220-Ohm Resistor (UV LED)
    - DHT11/22   - Relay 1 (Ch1)- G-V-S Rows
    - HC-SR04    - UV LED (Direct GPIO)
    - LDR
    - Gated Moisture
```

### A. Main Brain: ESP32 DevKit V1 (30-Pin)
* **Processor:** Xtensa Dual-Core 32-bit LX6 Microprocessor, running at **240 MHz**.
* **Memory:** 520 KB SRAM, 4 MB Flash.
* **Peripherals:** 12-bit ADCs (analog-to-digital converters), hardware timers, 3 hardware UART interfaces.
* **Why it exists:** Provides built-in Wi-Fi and Bluetooth on a single, high-speed chip. It has enough analog pins to read multiple sensors directly without needing any external multiplexers or co-processors like the Arduino Nano.
* **Power consumption:** ~80mA continuous (spikes up to 240mA during Wi-Fi transmission).

### B. Breakout Shield: Techtonics 30-Pin ESP32 Expansion Board
* **Interface:** Sits directly under the ESP32. Converts all 30 pins into Ground-VCC-Signal (G-V-S) header sets.
* **Power Jumper:** Has a yellow jumper cap. Set this jumper to **5V** so all V pins output a stable 5V (required for the relays and ultrasonic sensor).
* **Why it exists:** Solderless breadboards are highly unstable during public exhibitions. Bumping into the table can dislodge wires, shorting the board. The G-V-S shield allows all sensor cables to plug in securely using locked Female-to-Female ribbon cables, making the hardware **100% stable and shockproof**.

### C. Standalone Camera: AI-Thinker ESP32-CAM
* **Processor:** ESP32 WROVER Module with **4MB external PSRAM**.
* **Camera Sensor:** OV2640 2MP Lens with adjustable focus.
* **Programmer:** MB USB Programmer Shield. It snaps onto the back of the camera, translating serial lines to USB via an onboard CP2102 chip, and delivers stable 5V power over a Type-C cable.
* **Why it exists:** Handshakes wirelessly over Wi-Fi, completely eliminating the need for long, messy signal wires or ribbon cables stretching between your plant pot and your control deck.

### D. Sensors & Actuators
1. **DHT11/DHT22 (Ambient Temp/Humidity):** High-precision sensor using a single-bus digital interface (GPIO 4).
2. **2-Prong Soil Moisture Probe:** Analog resistive sensor. Connects its VCC to **GPIO 23** (power-gating pin) to prevent electrolysis and rust, and AO to **GPIO 34**.
3. **HC-SR04 (Ultrasonic Distance):** Emits a 40kHz sonar pulse to measure water height in the bucket (TRIG to GPIO 18, ECHO to GPIO 19).
4. **LDR Sensor:** Light-dependent resistor module. Outputs digital values (GPIO 14) indicating dark or bright states.
5. **Robocraze 5V Dual-Channel Relay Module:** Features optocoupler isolation, protecting your ESP32 pins from high back-EMF spikes when the pump turns on (IN1 connected to GPIO 5).
6. **5V Submersible Pump:** Brushless DC motor pump capable of lifting water up to 1 meter through silicone tubing.
7. **Everlight 5mm UV LED:** Purple ultraviolet LED emitting 395nm wavelength to promote plant leaf growth (directly driven via GPIO 12 with a 220-Ohm series resistor).

---

## ☁️ 2. Cloud Layer Specifications

### A. Firebase Realtime Database (RTDB)
* **What it is:** A cloud-hosted NoSQL database that synchronizes data across clients in real-time.
* **Why it exists:** RTDB holds an open WebSocket connection with both the ESP32 and the Next.js app. Telemetry writes and manual control changes are pushed instantly in **less than 100ms**, completely bypassing the slow polling delay of traditional SQL databases.
* **Database Rules:** Configured to allow public read/write access strictly to authenticated Anonymous sessions.

### B. Firebase Cloud Storage
* **What it is:** A secure Google Cloud Storage bucket designed for binary file storage.
* **Why it exists:** Houses the JPEG foliage scans uploaded on-request by the ESP32-CAM.
* **Capacity:** 5 GB free tier, allowing you to store over 80,000 SVGA plant scans.

---

## 💻 3. Application Layer Specifications

### A. Next.js Web Dashboard
* **Framework:** Next.js (App Router) deployed on **Vercel** (`https://verde-tech-proj.vercel.app/`).
* **UI Widgets:** Uses **Tailwind CSS** for layout grids and **Recharts** to plot live, glowing moisture line graphs.
* **Real-Time Client:** Hooks into the Firebase Web SDK, updating React state variables instantly when WebSocket changes are detected.

### B. Vercel Serverless APIs
* **Role:** Lightweight, global API routes that handle receiving binary image buffers from the ESP32-CAM, saving them to storage, fetching Delhi weather forecasts from OpenWeatherMap, and handshaking with Plant.id and Gemini 2.0 Flash.
