import os

# Create App directory
os.makedirs("App", exist_ok=True)

# ----------------------------------------------------
# 00_Project_Overview.md (Extreme Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/00_Project_Overview.md", "w") as f:
    f.write("""# 00. Project Overview & Technical Specification

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
""")

# ----------------------------------------------------
# 01_System_Architecture.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/01_System_Architecture.md", "w") as f:
    f.write("""# 01. System Architecture & Component Specifications

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
""")

# ----------------------------------------------------
# 02_Application_Workflow.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/02_Application_Workflow.md", "w") as f:
    f.write("""# 02. Complete Application Workflow & Logical Sequences

This document provides a highly detailed, step-by-step transaction workflow. It outlines what happens first, what happens next, who sends the data, who receives it, what format it is in, and what validations are performed.

---

## 🗺️ 1. Complete System Event Sequence

```
User App                  Firebase RTDB                 ESP32 Brain             ESP32-CAM
  │                            │                             │                       │
  │──(1. Anonymous Auth)──────►│                             │                       │
  │                            │                             │                       │
  │◄──(2. Connects WebSockets)─│                             │                       │
  │                            │◄──(3. Telemetry Upload)─────│                       │
  │◄──(4. Renders live gauges)─│                             │                       │
  │                            │                             │                       │
  │──(5. Click "Scan Leaf")───►│(Capture = true)             │                       │
  │                            │                             │                       │
  │                            │◄──(6. Reads Capture flag)───┼───────────────────────│
  │                            │                             │                       │
  │                            │                             │──(7. Flash & Capture)─►│
  │                            │                             │                       │
  │◄──(8. POSTs raw JPEG)──────┼─────────────────────────────┼───────────────────────│
  │                            │                             │                       │
  │──(9. Reset Capture flag)──►│(Capture = false)            │                       │
  │                            │                             │                       │
  │──(10. Plant.id & Gemini)──►│                             │                       │
  │                            │                             │                       │
  │◄──(11. Render AI Response)─│                             │                       │
```

---

## 📝 2. Step-by-Step Transaction Flow

### Step 1: User Loads the Application
* **Action:** User navigates to the Vercel-hosted URL: `https://verde-tech-proj.vercel.app/`.
* **Authentication Handshake:** The Next.js frontend runs the Firebase client SDK and attempts to sign in anonymously.
* **Data Format:** Secure JSON Web Token (JWT).
* **Validation:** Firebase Auth validates the request domain against your allowed list in the Firebase console.
* **If Auth Fails:** The app displays a red banner: *"❌ Connection Failed: Security token rejected. Reloading..."* and attempts to re-authenticate.

### Step 2: Renders the Dashboard
* **Action:** Next.js opens a permanent WebSocket stream to the `/Garden` path in Firebase RTDB.
* **Data Format:** WebSocket frames containing NoSQL JSON trees.
* **Telemetry Upload (ESP32):** The main **ESP32 DevKit** board reads its local sensors and writes a JSON payload under `/Garden` to Firebase every 1 second.
* **JSON Payload Format:**
  ```json
  {
    "Moisture": 52,
    "Temperature": 24.5,
    "Humidity": 65,
    "Light": "Dark",
    "TankLevel": 85
  }
  ```
* **Dashboard Render:** The app receives this telemetry in under 100ms, immediately updating the animated radial moisture ring, the ambient temp/humidity cards, and the blue water cylinder.

### Step 3: Changing a Parameter (Auto Threshold Slider)
* **Action:** The user slides the "Soil Moisture Target" slider on the dashboard to **45%**.
* **Database Write:** The Next.js app immediately writes `Threshold = 45` to the `/Garden` node of Firebase RTDB.
* **Data Format:** JSON numeric change.
* **Device Pull:** The ESP32 reads the updated threshold from Firebase over WebSockets.
* **Device Actuation:**
  1. The ESP32 compares the current soil moisture (e.g., 38%) against the new target (45%).
  2. Because the soil is dry, the ESP32 pulls **PUMP_RELAY LOW (ON)** (GPIO 5).
  3. The ESP32 writes `/Garden/Pump = "ON"` to Firebase, which instantly animates the pump icon on the user's screen.

### Step 4: On-Demand Camera Scan & AI Diagnostics
* **Action:** The user wants to scan a leaf for bugs or rust. They click the glowing **"Scan Plant Foliage"** button.
* **Trigger:** The app disables further manual clicks, starts a loading spinner, and writes `Capture = true` to Firebase `/Garden/Capture`.
* **Camera Detection:** The Standalone **ESP32-CAM** (polling Firebase every 2 seconds) reads the true flag.
* **Capture Execution:** The ESP32-CAM turns on its bright white flash LED, captures a single high-res snapshot, and turns the flash OFF immediately to prevent current-draw spikes.
* **Cloud Upload:** The ESP32-CAM posts the raw JPEG bytes to your Vercel serverless endpoint `/api/upload-photo`.
* **Database Updates:**
  1. The server receives the file, uploads it to Firebase Storage, and writes `Capture = false` back to Firebase to release the loading spinner.
  2. The server calls the **Plant.id API** to identify leaf spots/diseases.
  3. The server takes those diagnosis results, pings **Gemini 2.0 Flash**, and requests a conversational, monospace-styled remedy text.
  4. The Next.js app renders the leaf photo in its viewport and prints the Gemini AI diagnostic report directly inside the chatbot terminal.
""")

# ----------------------------------------------------
# 03_ESP32_Communication.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/03_ESP32_Communication.md", "w") as f:
    f.write("""# 03. ESP32 Communication Protocol

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
""")

# ----------------------------------------------------
# 04_ESP32_CAM_Workflow.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/04_ESP32_CAM_Workflow.md", "w") as f:
    f.write("""# 04. ESP32-CAM Workflow & Storage Pipeline

This document outlines the on-demand image capture, storage pipeline, and critical network routing configurations of the **ESP32-CAM** standalone vision node under the `/Garden` namespace.

---

## 📷 1. The On-Demand Camera Loop ("On Appeal")
The ESP32-CAM remains in a low-power, non-streaming idle state. It connects to Wi-Fi and polls the Firebase Realtime Database path `/Garden/Capture` every 2 seconds.

```
[ Next.js App ]             [ Firebase RTDB ]             [ ESP32-CAM ]             [ Vercel Cloud ]
       │                            │                            │                         │
       │──(Click "Scan")───────────►│                            │                         │
       │                            │(Capture = true)            │                         │
       │                            │◄──(Polls capture flag)─────│                         │
       │                            │                            │──(Flashes & Snaps)      │
       │                            │                            │                         │
       │                            │                            │──(POSTs Binary JPEG)───►│
       │                            │◄──(Resets flag to false)───┼─────────────────────────│
       │                            │                            │                         │
```

---

## 🚫 2. Why "Localhost" Must NEVER Be Used
A common beginner trap is configuring the ESP32-CAM's upload URL to point to a local computer address like `http://localhost:3000/api/upload-photo`.

* **The Problem:** The ESP32-CAM is an independent physical network computer with its own IP. When it requests `localhost`, it is requesting *itself* (not your laptop or server). The upload will immediately fail with a routing timeout!
* **The Solution (Production):** The ESP32-CAM must always post directly to your public, secure Vercel production domain:
  `https://verde-tech-proj.vercel.app/api/upload-photo`
* **The Solution (Local Testing):** If testing locally over your mobile hotspot, the camera must be configured to point to your laptop's exact local hotspot IP address (e.g., `http://192.168.1.6:5000/upload`).

---

## ⚡ 3. The 8MHz Clock Throttling Workaround (Antenna RF Fix)

On cheap or standard ESP32-CAM clone boards, running the camera's internal master clock (`XCLK`) at the default **20MHz** creates a fatal design flaw:

* **The Interference:** A 20MHz clock frequency generates **intense high-frequency electromagnetic interference** directly with the adjacent onboard PCB Wi-Fi antenna!
* **The Symptom:** When taking a photo and transmitting over Wi-Fi at the same time, the Wi-Fi radio drops packets, resulting in `send payload failed` errors and connection dropouts.
* **The Solution:** Throttle the clock speed down to **`8000000` (8MHz)** or **`10000000` (10MHz)** in the camera configuration:
  ```cpp
  config.xclk_freq_hz = 8000000; // 8MHz clock completely stops RF Wi-Fi interference!
  ```
* **Benefits:** This drops the peak current draw by 40%, completely preventing current-draw brownouts (such as `0x20002` errors) and allowing the camera to transmit smoothly over Wi-Fi with 100% stability!

---

## 💾 4. Direct Upload vs. Backend Request Comparison

| Metric | Option A: Standalone Camera Server | Option B: Direct HTTP POST Upload (Recommended) |
| :--- | :--- | :--- |
| **How it works** | Camera hosts local IP server; app opens stream. | Camera snaps on request and POSTs image to server. |
| **Pros** | Real-time continuous live streaming. | **Incredibly low power, zero network blocks, extremely secure.** |
| **Cons** | **Fails on Home Broadband (AP Isolation blocks it)**; heats up. | Requires a backend upload endpoint. |

**Decision:** **Option B (Direct HTTP POST Upload)** is chosen for the production build because it completely bypasses AP/Client isolation on home Wi-Fi routers and keeps the board cool!
""")

# ----------------------------------------------------
# 05_Backend_Architecture.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/05_Backend_Architecture.md", "w") as f:
    f.write("""# 05. Next.js Backend & Serverless API Routes

This document details the serverless backend architecture running on **Vercel** to support **Project Verde V3.0**.

---

## ⚙️ 1. API Runtimes & Execution Boundaries
We utilize two distinct serverless execution environments on Vercel:

### A. Next.js Edge Runtime (Ultra-Low Latency)
Used for fast API routing, weather synchronizations, and database triggers. It runs on lightweight V8 engines distributed globally, achieving sub-50ms execution times.

### B. Standard Node.js Runtime (Heavy Processing)
Used for raw binary image handling, buffer manipulation, and file-streaming directly to Firebase Storage.

---

## 🔌 2. API Endpoint Specifications

### A. Photo Upload Endpoint
* **Path:** `/api/upload-photo`
* **Runtime:** Standard Node.js
* **Logic:** Receives raw binary JPEG buffers from the ESP32-CAM. Uses the `firebase-admin` SDK to write the image directly to your Firebase Storage bucket under the path `/scans/{userId}/current_capture.jpg`.
* **Security:** Validates the presence of an `x-api-key` header to prevent storage spamming.

### B. Plant Disease Diagnosis
* **Path:** `/api/analyze-plant`
* **Runtime:** Edge Runtime
* **Logic:** Receives the newly uploaded image URL. Sends it to **Plant.id** to extract the botanical genus and leaf disease confidence scores.
* **AI Chat Integration:** Feeds those diagnosis results directly into **Gemini 2.0 Flash** with a system prompt to output friendly, monospace-styled organic treatment steps to the dashboard's chat console.

### C. Weather Forecast Sync
* **Path:** `/api/weather-sync`
* **Runtime:** Edge Runtime
* **Logic:** Triggered via a Vercel cron schedule once an hour. Fetches current weather for Delhi (`LAT: 28.6139° N, LON: 77.209° E`) from the **OpenWeatherMap API**. 
  * If `"rain"`, `"drizzle"`, or `"thunderstorm"` is found, writes `weather_override = 1` in Firebase under `/Garden/WeatherOverride`.
  * If clear, writes `weather_override = 0`.
""")

# ----------------------------------------------------
# 06_Supabase_vs_Firebase.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/06_Supabase_vs_Firebase.md", "w") as f:
    f.write("""# 06. Supabase vs. Firebase Comparison

This document provides a professional, deep architectural comparison between **Firebase Realtime Database** and **Supabase (PostgreSQL)** for the execution of our smart garden IoT prototype.

---

## 📊 1. Face-to-Face Technical Comparison

| Feature Metric | Firebase (Realtime Database) | Supabase (PostgreSQL) |
| :--- | :--- | :--- |
| **Real-Time Latency** | WebSocket-based native sync (**<100ms**). | Realtime triggers on Postgres WAL. |
| **Microcontroller Support**| Lightweight, highly stable `Firebase-ESP32` SDK. | Complex manual REST/JWT header assembly. |
| **Storage Allocation** | **5 GB** completely free. | **1 GB** completely free. |
| **Database Rules** | Simple JSON paths, extremely easy to audit. | SQL-based Row Level Security (RLS) policies. |
| **Data Format** | Single JSON Document Tree. | Relational SQL Tables & Foreign keys. |
| **Authentication** | Built-in Anonymous & Email Auth. | GoTrue Go-based Auth schemas. |

---

## 🏆 2. Architectural Recommendation: Firebase RTDB

**Firebase Realtime Database (RTDB) is selected as the database of choice.**

### Deep Technical Justifications:
1. **Processor Overhead & Memory Constraints:** The ESP32 is a low-power microcontroller. Running a SQL-based ORM or assembling complex HTTP POST headers with JWT authorization strings for Supabase's Postgres API uses significant RAM, leading to **heap allocation failures** and crashes. The Mobizt `FirebaseESP32` client handles SSL/TLS handshakes internally with extreme stability.
2. **Sub-100ms Manual Toggles:** Firebase RTDB holds a persistent, open WebSocket stream with the ESP32. When you click "Force ON" on the app, the state change travels over the air and triggers the pump relay in **less than 100ms**. Supabase’s PostgreSQL real-time engine, while robust, introduces several database layers (Write-Ahead Log listener -> realtime server -> client), resulting in higher latency and slower, clunky physical responses during live demos.
3. **Generous Storage Free Tier:** Firebase offers **5 GB** of cloud storage completely free, which is 5x larger than Supabase's 1 GB free tier. This allows you to store thousands of leaf scans without running out of space!
""")

# ----------------------------------------------------
# 07_Database_Design.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/07_Database_Design.md", "w") as f:
    f.write("""# 07. Database Design & JSON Schema

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
""")

# ----------------------------------------------------
# 08_API_Design.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/08_API_Design.md", "w") as f:
    f.write("""# 08. API Endpoint Specifications

This document outlines the REST API routes running on Vercel to support the Next.js frontend and ESP32-CAM nodes.

---

## 🔌 1. API Endpoint Reference

### A. Image Upload Route
* **Endpoint:** `POST /api/upload-photo`
* **Runtime:** Node.js (Buffer handling)
* **Headers:**
  * `Content-Type: image/jpeg`
  * `x-api-key: your-secure-cam-key` (Prevents unauthorized image uploads)
* **Request Body:** Raw binary JPEG image buffer.
* **Success Response (200 OK):**
```json
{
  "success": true,
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/verde-project.appspot.com/o/scans%2Fcurrent.jpg"
}
```
* **Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Invalid API Key header"
}
```

### B. Plant Leaf AI Diagnosis
* **Endpoint:** `POST /api/analyze-plant`
* **Runtime:** Edge Runtime
* **Headers:**
  * `Content-Type: application/json`
* **Request Body:**
```json
{
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/verde-project.appspot.com/o/scans%2Fcurrent.jpg"
}
```
* **Success Response (200 OK):**
```json
{
  "plant_identified": "Ocimum tenuiflorum (Tulsi)",
  "health_diagnosis": "Leaf Spot Disease (89% confidence)",
  "gemini_remedy": "Fungus spots detected. Spray organic neem-oil water mixture weekly, and reduce moisture threshold to 40%."
}
```

### C. Weather Forecast Sync
* **Endpoint:** `GET /api/weather-sync`
* **Runtime:** Edge Runtime
* **Description:** Hourly cron schedule. Fetches forecast for Delhi from OpenWeatherMap and writes `weather_override` to Firebase.
* **Success Response (200 OK):**
```json
{
  "success": true,
  "weather": "Rain",
  "override_written": 1
}
```
""")

# ----------------------------------------------------
# 09_Authentication.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/09_Authentication.md", "w") as f:
    f.write("""# 09. User Authentication & Session Lifecycles

This document outlines the authentication and tokenization strategy for **Project Verde V3.0**.

---

## 🔑 1. Strategy: Firebase Anonymous Authentication

For a competitive live exhibition (DAV ACON 5), the judges will only interact with your app for 2 to 3 minutes. **Asking them to register, type passwords, or verify emails will kill your presentation flow.**

We utilize **Firebase Anonymous Authentication**:
* **How it works:** When the web app loads, it instantly creates a temporary, unique authenticated session in the background without requiring any user input.
* **Security Benefits:** This generates a secure JWT token inside the browser, allowing the client to securely read/write to the Firebase RTDB while fully obeying your strict Database Security Rules.

---

## 🛠️ 2. Step-by-Step Implementation

1. **Install Firebase SDK:**
   `npm install firebase`
2. **Initialize Auth Client:**
```javascript
// lib/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, signInAnonymously } from "firebase/auth";

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  databaseURL: "YOUR_DATABASE_URL",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export const initializeUserSession = async () => {
  try {
    const userCredential = await signInAnonymously(auth);
    console.log("Anonymous UID:", userCredential.user.uid);
    return userCredential.user;
  } catch (error) {
    console.error("Session init failed:", error);
    return null;
  }
};
```

---

## 🔄 3. Token Session Lifecycles
* **Persistence:** The session token is automatically cached in the browser's `IndexedDB` storage by the Firebase Web SDK. If the judge reloads your page, the session is preserved instantly.
* **Revocation:** If the user closes the page, the anonymous session remains valid for 30 days before automatically expiring, ensuring your database remains secure and clutter-free.
""")

# ----------------------------------------------------
# 10_Row_Level_Security.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/10_Row_Level_Security.md", "w") as f:
    f.write("""# 10. Database Rules & RLS Security

This document details the security rules deployed on your Firebase Realtime Database and Cloud Storage buckets to secure your data.

---

## 🔒 1. Firebase Realtime Database Security Rules

These rules ensure that only authenticated sessions (such as your Next.js app running under Anonymous Auth, or your ESP32 board using a secure Master Secret Key) can read and write to your nodes.

```javascript
{
  "rules": {
    "Garden": {
      // Only authenticated users can read sensor values
      ".read": "auth != null",
      // Only authenticated users/ESP32 can write telemetry
      ".write": "auth != null"
    }
  }
}
```

---

## 🔒 2. Firebase Cloud Storage Security Rules

To ensure leaf scans are securely handled while allowing public rendering on your Next.js dashboard viewport, set these rules on your Storage buckets:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      // Leaf scans are publicly readable so your dashboard can load images via URLs
      allow read: if true;
      
      // Only authenticated users or your backend API can write photos
      allow write: if request.auth != null;
    }
  }
}
```

---

## 🕵️‍♂️ 3. Best Practices
* **No Public Writing:** Never leave rules set to `".write": "true"` in production. This leaves your water pump and grow lights completely open to anyone on the internet who scans your website!
* **Secret Rotation:** Store your Firebase Admin secret keys securely inside Vercel environment variables, and never commit them to public GitHub repositories.
""")

# ----------------------------------------------------
# 11_Image_Handling.md (Ultimate Detail aligned with /Garden)
# ----------------------------------------------------
with open("App/11_Image_Handling.md", "w") as f:
    f.write("""# 11. Image Handling & Storage Lifecycle

This document outlines the end-to-end binary buffer upload, compression, and automated cleanup (TTL) pipeline of plant leaf photographs.

---

## 📦 1. The Image Upload Pipeline

```
[ ESP32-CAM ]               [ Next.js API ]               [ Firebase Storage ]
      │                            │                               │
      │──(1. POSTs raw JPEG)──────►│                               │
      │   Buffer in RAM            │                               │
      │                            │──(2. Streams binary buffer)──►│
      │                            │   File: current_capture.jpg   │
      │◄──(3. Returns 200 OK)──────┼───────────────────────────────│
```

### Steps:
1. **On-Demand Snap:** ESP32-CAM captures a JPEG frame at `SVGA (800x600)` with `jpeg_quality = 10` to keep the file size very small (~60 KB), preventing Wi-Fi packet drops.
2. **Buffer Stream:** The camera posts the raw binary JPEG bytes directly to the `/api/upload-photo` Vercel route over WiFi.
3. **Storage Save:** The Next.js API receives the binary buffer and streams it straight to Firebase Storage under the folder: `/scans/{userId}/current_capture.jpg`.

---

## 🗑️ 2. The 15-Day Auto-Delete Lifecycle Policy (TTL)

To prevent your 5GB free storage tier from filling up, you must implement an automated **Time-To-Live (TTL)** cleanup routine. We write a serverless Vercel cron route that runs once every night:

```javascript
// app/api/cleanup-storage/route.js
import { getStorage } from "firebase-admin/storage";
import { NextResponse } from "next/server";

export async function GET(request) {
  try {
    const bucket = getStorage().bucket();
    const [files] = await bucket.getFiles({ prefix: "scans/" });
    
    const fifteenDaysAgo = Date.now() - (15 * 24 * 60 * 60 * 1000);
    let deletedCount = 0;
    
    for (const file of files) {
      const [metadata] = await file.getMetadata();
      const createdTime = new Date(metadata.timeCreated).getTime();
      
      if (createdTime < fifteenDaysAgo) {
        await file.delete();
        deletedCount++;
      }
    }
    
    return NextResponse.json({ success: true, deleted: deletedCount });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
```
* **Benefit:** This keeps your storage footprint incredibly low, meaning your 5GB free tier will **never run out of space**!
""")

# ----------------------------------------------------
# 12_Offline_and_Error_Handling.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/12_Offline_and_Error_Handling.md", "w") as f:
    f.write("""# 12. Offline and Error Handling

This document outlines the hard-fault, network drop, and device-offline recovery strategies designed into the system.

---

## 🚨 1. Hard-Fault Recovery Scenarios

### A. ESP32 Main Brain Offline
* **Trigger:** Next.js dashboard detects that the sensor `last_updated` timestamp in Firebase RTDB is older than 10 seconds.
* **App Display:** The dashboard displays a red pulsing badge: *"⚠️ EDGE OFFLINE: System operating autonomously"*. It freezes the manual control switches to prevent user command congestion.
* **Local Recovery:** The ESP32 continues running its local, independent loops. If soil moisture falls below target, it still waters locally, ensuring your plant survives even if Wi-Fi dies!

### B. ESP32-CAM Capture Failure (Brownout/Voltage Sag)
* **Trigger:** Next.js API times out waiting for the binary POST upload from the camera.
* **App Display:** The app sets `/Garden/Capture = false` in Firebase, stops the user loading spinner, and slides in an error toast: *"❌ Scan Failed: Insufficient power on camera node. Retrying..."*
* **Local Recovery:** ESP32-CAM clears its frame buffer RAM instantly using `esp_camera_fb_return(fb)` to prevent memory leaks and crashes, returning to its idle state.

---

## 🛠️ 2. Network State Recovery Matrix

| Fault State | Consequence | App UI Behavior | Physical Device Behavior |
| :--- | :--- | :--- | :--- |
| **Hotspot Offline** | No data reaches Firebase. | Displays "Device Offline" with last cached values. | ESP32 runs autonomous watering locally; retries WiFi every 5s. |
| **Database Down** | Controls cannot be synced. | Displays "Cloud Sync Error" banner. | ESP32 falls back to local threshold controls. |
| **User Closes App** | Manual actions stop. | N/A (Session preserved). | ESP32 instantly reverts to autonomous smart watering. |
""")

# ----------------------------------------------------
# 13_Notifications.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/13_Notifications.md", "w") as f:
    f.write("""# 13. System Notifications & Alarms

This document outlines the system-level alarm configurations and notification flows designed for **Project Verde V3.0**.

---

## 🚨 1. Critical Alarm Flows

### A. Water Reservoir Empty (Dry Run Prevention)
* **Trigger:** The HC-SR04 ultrasonic sensor reads water depth $<10\\%$ in the bucket.
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
""")

# ----------------------------------------------------
# 14_UI_UX_Guidelines.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/14_UI_UX_Guidelines.md", "w") as f:
    f.write("""# 14. UI/UX Guidelines & Themes

This document outlines the design language, screens, and accessible components of the **Verde Web Client**.

---

## 🎨 1. Monospace Cyberpunk Aesthetic
To match your portfolio and tech exhibition theme, the dashboard utilizes a high-tech dark-green console theme:

* **Background:** Solid matte black (`#0c0c0c` / `#121212`).
* **Highlights:** Glowing botanical neon green (`#22c55e`).
* **Typography:** Clean monospace fonts (`Share Tech Mono`, `Courier Prime`).
* **Hover Glows:** Hovering over elements triggers a subtle box shadow glow:
  `box-shadow: 0 0 15px rgba(34,197,94,0.3)`

---

## 📊 2. Screen Hierarchy (Single-Page Dashboard)

The app is structured as a single-page responsive grid (`grid-cols-1 lg:grid-cols-12`):

### A. Widget Row (Top)
* **State Badge:** Shows whether the ESP32 is online, offline, or connecting.
* **Weather Sync Badge:** Renders local weather in Delhi (e.g. *"⛅ Delhi: Sunny"*).

### B. Live Telemetry Column (Left - 4 Columns)
* **Moisture Dial:** A radial circular gauge showing exact soil moisture %.
* **Reservoir Cylinder:** A blue-gradient liquid bar showing remaining bucket water % (derived from ultrasonic readings).
* **Temp/Hum Cards:** Monospace values for ambient metrics.

### C. Live History Chart (Center - 5 Columns)
* **Recharts AreaChart:** A glowing green line chart plotting moisture levels over the last 24 hours.

### D. Manual Override Panel (Right - 3 Columns)
* **Toggles:** Manual/Auto mode toggle.
* **Trigger Slider:** 0-100% target slider (sets `moisture_threshold`).
* **Actuator Buttons:** Forced Pump Trigger, Forced Grow Light Trigger.

### E. AI Diagnostic Deck (Bottom - 12 Columns)
* **Foliage Viewport:** Displays the captured JPEG leaf scan.
* **AI Bot Terminal:** A dark green monospace terminal chat window showing Gemini 2.0 leaf disease reports.
""")

# ----------------------------------------------------
# 15_Project_Rules.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/15_Project_Rules.md", "w") as f:
    f.write("""# 15. Strict Project Rules

Any developer (including Anuj) or AI companion writing code for **Project Verde V3.0** must strictly obey these absolute constraints.

---

## 🛑 1. Absolute Constraints

1. **NEVER Use Localhost for Production Node Communication:**
   * The ESP32-CAM cannot upload files to `http://localhost:3000`. You must use your public Vercel production domain:
     `https://verde-tech-proj.vercel.app/api/upload-photo`
2. **NEVER Hardcode Secrets or Keys:**
   * Firebase secrets, OpenWeatherMap tokens, and Gemini API keys must **never** be written in your codebase. They must always be loaded via Vercel's Server Environment variables (`process.env`).
3. **NEVER Let the Soil Sensor Corrode:**
   * You must write power-gating logic in your ESP32 code. Never leave the 2-prong sensor's VCC connected to the constant 5V rail. It must only power up for 15ms during reads.
4. **ALWAYS Enable PSRAM on Camera compiles:**
   * Make sure your AI-Thinker ESP32-CAM compilation has PSRAM active, or the camera frame allocation will fail.
5. **ALWAYS Handle Device Offline States:**
   * If the ESP32 goes offline, your dashboard must display cached database values cleanly and mark the device status as "Offline" with a red pulsing badge.
""")

# ----------------------------------------------------
# 16_Best_Practices.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/16_Best_Practices.md", "w") as f:
    f.write("""# 16. Professional Best Practices

This document outlines the coding standards, folder layouts, and performance optimization practices.

---

## 📂 1. Directory Structure

```text
next-app/
├── app/
│   ├── api/
│   │   ├── upload-photo/   # Camera upload API (Node.js buffer)
│   │   ├── analyze-plant/  # Plant.id + Gemini API route (Edge)
│   │   └── weather-sync/   # OpenWeatherMap cron route (Edge)
│   ├── dashboard/          # Next.js main web client
│   └── page.js             # Landing splash page
├── components/             # Reusable UI widgets
├── lib/
│   └── firebase.js         # Firebase client config
└── public/                 # Static assets
```

---

## 🚀 2. Code Organization & Performance

* **Try/Catch Blocks:** All API routes must wrap calls in try/catch blocks and return clean error JSON payloads.
* **Component Lazy Loading:** Large UI components (like the Recharts AreaChart) must be lazy-loaded to prevent sluggish page paint times on low-end devices.
* **Tailwind Class Merging:** Utilize `clsx` or `tailwind-merge` for clean, modular, and dynamic class allocations in your React components.
""")

# ----------------------------------------------------
# 17_Future_Improvements.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/17_Future_Improvements.md", "w") as f:
    f.write("""# 17. Future Improvements & Scalability

These scalable future expansions can be added to your slides or code after the DAV ACON 5 competition:

---

## 📈 1. Predictive Irrigation Modeling
* **Concept:** Use a machine learning algorithm (like a simple Linear Regression or a lightweight TensorFlow model) to study the soil moisture depletion rate under different temperatures.
* **Benefit:** Predicts *exactly* how many hours are left before the plant next needs water, displaying: *"Next irrigation cycle predicted in 3 hours."*

---

## 🍇 2. Multi-Farm / Multi-Greenhouse Clusters
* **Concept:** Upgrade your NoSQL tree structure to support a list of device MAC addresses under a single user profile.
* **Benefit:** Allows a farmer to manage multiple distinct greenhouse zones or crop beds from a single web client.

---

## ⛅ 3. Deep Weather Forecast API Integration
* **Concept:** Fetch 3-day humidity and temperature forecasts.
* **Benefit:** Adjusts irrigation amounts dynamically (e.g. if the next day is forecasted to be extremely hot, irrigate 15% more today to protect the roots).
""")

# ----------------------------------------------------
# 18_Development_Checklist.md (Ultimate Detail)
# ----------------------------------------------------
with open("App/18_Development_Checklist.md", "w") as f:
    f.write("""# 18. Development Implementation Checklist

Use this checklist to track your development progress step-by-step.

---

## 🏁 Phase 1: Firebase Project Setup
* [ ] Create a new project on the Firebase Console.
* [ ] Initialize a **Realtime Database** (RTDB) in test mode.
* [ ] Enable **Firebase Cloud Storage** (default bucket).
* [ ] Enable **Anonymous Authentication** in the Auth tab.
* [ ] Add your API keys and RTDB URL to your Next.js `.env.local` file.

## 🏁 Phase 2: Next.js Web Client Setup
* [ ] Initialize Next.js project using `npx create-next-app@latest`.
* [ ] Install core dependencies: `firebase`, `recharts`, `framer-motion`, `lucide-react`.
* [ ] Create your `lib/firebase.js` initialization script.
* [ ] Set up background Anonymous authentication on dashboard load.

## 🏁 Phase 3: Telemetry Gauges & Chart
* [ ] Create the radial moisture ring gauge.
* [ ] Create the filling blue water reservoir cylinder (from `tank_level`).
* [ ] Add the Temperature, Humidity, and Lux card widgets.
* [ ] Implement the Recharts `AreaChart` plotting live moisture logs.

## 🏁 Phase 4: Overrides & Firebase Cloud Sync
* [ ] Bind your Manual/Auto toggle switch to change `manual_mode` in Firebase RTDB.
* [ ] Bind your target threshold slider to change `moisture_threshold` in Firebase.
* [ ] Set up the serverless OpenWeatherMap weather check endpoint.

## 🏁 Phase 5: Camera & AI Integrations
* [ ] Code the Next.js `/api/upload-photo` endpoint to handle binary image streams.
* [ ] Bind your "Scan Foliage" dashboard button to write `capture_photo = true` in Firebase.
* [ ] Code the `/api/analyze-plant` route (connecting Plant.id and Gemini 2.0 Flash APIs).
* [ ] Embed the captured photo and Gemini response into the dashboard's AI chatbot console.
""")

print("Successfully written all handoff documentation files under /home/user/App/!")
