import os

# Create App directory
os.makedirs("App", exist_ok=True)

# ----------------------------------------------------
# 1. 00_Project_Overview.md
# ----------------------------------------------------
with open("App/00_Project_Overview.md", "w") as f:
    f.write("""# 00. Project Overview

## 🎯 1. Project Goal
The core objective of **Project Verde V3.0 (Autonomous Plant OS)** is to build an industrial-grade, low-cost, smart residential gardening and precision agritech system. It enables remote, automated, and AI-assisted plant care from anywhere in the world. By shifting from a complex co-processing system to a single-brain WROOM-32 platform, the project achieves maximum reliability, stable wireless operations, and an extremely neat, non-messy physical build.

## 👥 2. Target Users & Expected Audits
* **Residential Gardeners:** Individuals who need to monitor plant hydration, soil health, and light exposure while away from home for extended periods.
* **School & Tech Exhibition Judges:** Evaluators at the **DAV ACON 5** competition who require deep scientific merit, robust electrical design, zero-error execution, and direct, practical agritech utility.
* **Agritech Enthusiasts:** Users seeking low-power, automated crop-environment control systems with real-time browser telemetry.

## ⚙️ 3. Key System Components & Tech Stack
The physical and digital systems are decoupled into distinct operational boundaries:

### A. Edge Node (Main Brain & Sensors)
* **Microcontroller:** Single ESP32 DevKit V1 (30-pin, CP2102 driver, Type-C interface).
* **Breakout Shield:** Techtonics 30-Pin Breakout Expansion Board (Yellow jumper on 5V).
* **Sensors:** 
  * DHT22/AM2302 (Ambient Temperature & Humidity).
  * 2-Prong Resistive Soil Moisture Sensor (with VCC gated via GPIO 23 to prevent corrosion).
  * LDR Analog Light Sensor (Luminosity tracking).
  * HC-SR04 Ultrasonic Distance Sensor (Water reservoir level tracking).
* **Actuators:**
  * 5V Submersible Water Pump (controlled via Channel 1 of a 5V Optocoupler-Isolated Relay).
  * Everlight 5mm UV LED (Photosynthetic growth light, driven directly via GPIO 26 with a 220-Ohm series resistor).

### B. Vision Node (On-Demand AI Camera)
* **Controller:** AI-Thinker ESP32-CAM with OV2640 2MP Lens.
* **Programmer:** MB USB Programmer Shield (Snaps onto the back of the camera, provides direct USB connection).
* **Clock Configuration:** Clock throttled down to **8MHz** to completely eliminate Wi-Fi RF antenna interference.

### C. Real-Time Cloud Sync & Storage
* **Realtime Database:** Firebase Realtime Database (RTDB) serving as the sub-100ms WebSocket synchronization layer.
* **Cloud Storage:** Firebase Storage (5GB Free Tier) holding on-demand plant leaf scans.
* **Authentication:** Firebase Anonymous Authentication to enable instant, password-free dashboard loads.

### D. Next.js Web Client (Dashboard)
* **Frontend:** Next.js (App Router), Tailwind CSS, Framer Motion, Recharts.
* **Hosting:** Vercel (`https://verde-tech-proj.vercel.app/`).
* **API Handshakes:** Plant.id API (visual leaf pathogen identification) + Gemini 2.0 Flash API (conversational treatment advisor).

---

## 🗺️ 4. System Boundaries & Logical Flows

```
 +-------------------------------------------------------------------------------------------------+
 |                                     PHYSICAL SYSTEM BOUNDARY                                    |
 |                                                                                                 |
 |  [ ESP32-CAM Vision Node ]                           [ ESP32 Main Control Deck ]                |
 |  - Powered via USB-C on MB Shield                    - Powered via USB-C on Expansion Shield    |
 |  - Standalone Wi-Fi Connection                       - Gated 2-Prong Moisture, DHT22, HC-SR04   |
 |  - Idle until Firebase trigger                       - Standard 4s Telemetry stream             |
 |                                                                                                 |
 +----------------────────────────┬────────────────────────────────┬────────────────---------------+
                                  │                                │
                             (WiFi Sync)                      (WiFi Sync)
                                  ▼                                ▼
 +----------------────────────────────────────────────────────────────────────────────────────────-+
 |                                       CLOUD SYSTEM BOUNDARY                                     |
 |                                                                                                 |
 |                            [ Firebase Realtime Database (RTDB) ]                                |
 |                            - Real-time JSON Tree Synchronization                                |
 |                            - Handshakes, Toggles, Thresholds, and Telemetry                     |
 |                                                                                                 |
 +----------------───────────────────────────────┬────────────────────────────────────────────────-+
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
# 2. 01_System_Architecture.md
# ----------------------------------------------------
with open("App/01_System_Architecture.md", "w") as f:
    f.write("""# 01. System Architecture & Topology

This document details the multi-tier architectural design of **Project Verde V3.0**. The topology is split into three main layers: **Edge Layer**, **Cloud Layer**, and **Application Layer**, ensuring modularity, high performance, and error isolation.

---

## 🌐 1. High-Level System Topology

```
+─────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                           APPLICATION LAYER                                         |
|                                                                                                     |
|  +───────────────────────────────────────+          +────────────────────────────────────────────+  |
|  |           Next.js Frontend            |  ◄====►  |            Vercel Serverless               |  |
|  |     (Tailwind CSS + Recharts UI)      |  (HTTPS) |     (Upload, Weather & AI API Routes)      |  |
|  +───────────────────────────────────────+          +────────────────────────────────────────────+  |
|                      ▲                                                    │                         |
|                      │                                                    │                         |
|                 (WebSockets)                                       (REST API Calls)                 |
|                      ▼                                                    ▼                         |
+──────────────────────┼────────────────────────────────────────────────────┼─────────────────────────+
|                      │                    CLOUD LAYER                     │                         |
|                      ▼                                                    ▼                         |
|  +───────────────────────────────────────+          +────────────────────────────────────────────+  |
|  |       Firebase Realtime DB            |          |            Firebase Storage                |  |
|  |  (sub-100ms WebSocket state sync)     |          |       (5GB Free Tier - Scans Folder)       |  |
|  +───────────────────────────────────────+          +────────────────────────────────────────────+  |
|                      ▲                                                    ▲                         |
|                      │                                                    │                         |
|                 (WiFi Sync)                                          (HTTP POST)                    |
|                      ▼                                                    │                         |
+──────────────────────┼────────────────────────────────────────────────────┼─────────────────────────+
|                      │                     EDGE LAYER                     │                         |
|                      ▼                                                    │                         |
|  +───────────────────────────────────────+                                │                         |
|  |         ESP32 Main Brain              |                                │                         |
|  |     (DOIT DevKit V1 + Shield)         |                                │                         |
|  |  [Moisture, DHT22, HC-SR04, Relay]    |                                │                         |
|  +───────────────────────────────────────+                                │                         |
|                                                                           │                         |
|  +───────────────────────────────────────+                                │                         |
|  |         ESP32-CAM Node                | ───────────────────────────────┘                         |
|  |     (Standalone AI Camera)            |                                                          |
|  +───────────────────────────────────────+                                                          |
+─────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 🛠️ 2. Detailed Technical Layering

### A. The Edge Layer (Hardware Modules)
* **The Master Brain (ESP32 DevKit V1):** Sits on the **Techtonics Breakout Shield**. It functions entirely autonomously. It reads sensor data, manages the local control loop, and syncs variables over WiFi with Firebase RTDB.
* **The Vision Node (ESP32-CAM):** Operates on an independent power supply, physically separated from the main deck. It sleeps in an idle polling state, connects directly to WiFi, and uploads a high-resolution snapshot only when triggered by the database.
* **The Breakout Shield (Techtonics):** Eliminates loose breadboard connections by breaking out every GPIO pin into Ground-VCC-Signal (G-V-S) header sets.

### B. The Cloud Layer (Sync & Storage)
* **Firebase Realtime Database (RTDB):** Maintains an open, persistent WebSocket connection with both the Next.js client and the ESP32. Changes on either side (e.g., toggling a switch on the app or reading a new temperature value on the ESP32) are synced in less than 100 milliseconds.
* **Firebase Cloud Storage:** Houses the JPEG leaf pictures uploaded by the ESP32-CAM.
* **Firebase Authentication:** Handles Anonymous token generation to protect storage bucket write access.

### C. The Application Layer (Frontend & Serverless APIs)
* **The Next.js Web App:** Built using React and Tailwind CSS, hosted on Vercel. Connects to Firebase RTDB over WebSockets. Renders real-time telemetry gauges, interactive threshold sliders, historical line graphs, and the AI chatbot terminal.
* **Vercel Serverless Functions:** Lightweight Node.js API routes that handle receiving binary image buffers from the ESP32-CAM, pushing assets to Firebase Storage, fetching Delhi weather forecasts from OpenWeatherMap, and compiling diagnostics via Plant.id and Gemini 2.0 Flash.

---

## 🔒 3. Architectural Design Decisions

### Why Single-Brain ESP32?
* *The Previous Setup:* Master-Slave link (Nano as sensor hub, NodeMCU as gateway) connected via SoftwareSerial with 1k/2k-Ohm resistor level shifters.
* *The Problem:* Extremely messy breadboard layout (25+ wires), prone to connection dropouts, high serial latency, and lacks native hardware serial lines.
* *The Solution:* Shifting to a single **ESP32 WROOM-32**. It features a 240MHz dual-core CPU, multi-channel ADC pins, built-in WiFi, and hardware serial ports. This eliminates the Nano, SoftwareSerial libraries, logic-level resistors, and breadboard clutter completely!

### Why Standalone Wireless ESP32-CAM?
* *The Problem:* Long, messy ribbon cables extending from the central cardboard deck to the plant's leaf rim can drop signals, collect electrical noise, and look unpolished.
* *The Solution:* The ESP32-CAM operates as an **independent, wireless network node**. It connects to your hotspot, power-gates its lens and flash, and communicates with the main brain strictly through the cloud (Firebase RTDB). This creates a highly advanced, wire-free **Distributed IoT Mesh** that will score maximum points with competitive exhibition judges!
""")

# ----------------------------------------------------
# 5. 02_Application_Workflow.md
# ----------------------------------------------------
with open("App/02_Application_Workflow.md", "w") as f:
    f.write("""# 02. Application Workflow & Sequence

This document defines the step-by-step transaction flow across your entire system, from user interaction to hardware execution and cloud database sync.

---

## 🗺️ 1. Complete System Sequence Map

```
[ User App ]              [ Firebase RTDB ]            [ ESP32 Brain ]            [ ESP32-CAM ]
     │                            │                           │                          │
     │──(1. Login/Anon Auth)─────►│                           │                          │
     │                            │                           │                          │
     │◄──(2. Subscribes WebSocket)│                           │                          │
     │                            │◄──(3. Telemetry Stream)───│                          │
     │◄──(4. Renders live gauges)─│                           │                          │
     │                            │                           │                          │
     │──(5. Slider Adjust: 45%)──►│(threshold = 45)           │                          │
     │                            │◄──(6. Reads threshold)────│                          │
     │                            │                           │                          │
     │──(7. Click "Scan Leaf")───►│(capture_photo = true)     │                          │
     │                            │                           │                          │
     │                            │◄──(8. Reads capture flag)─┼──────────────────────────│
     │                            │                           │                          │
     │                            │                           │──(9. Flash & Capture)───►│
     │                            │                           │                          │
     │◄──(10. POSTs raw JPEG)─────┼───────────────────────────┼──────────────────────────│
     │                            │                           │                          │
     │──(11. Reset capture flag)─►│(capture_photo = false)    │                          │
     │                            │                           │                          │
     │──(12. Plant.id & Gemini)──►│                           │                          │
     │                            │                           │                          │
     │◄──(13. Render AI Remedy)───│                           │                          │
```

---

## 📝 2. Step-by-Step Transaction Flow

### Step 1: User Opens App & Authenticates
* **Action:** The Next.js frontend is loaded by the user.
* **Trigger:** The app instantly runs the Firebase Web SDK and registers a secure **Anonymous Session**.
* **Result:** Firebase returns an auth token, granting the browser secure, restricted read/write access to the database paths.

### Step 2: Live Telemetry Initialization
* **Action:** The app dashboard establishes a permanent WebSocket listener to the path `/sensors` in Firebase RTDB.
* **Hardware Push:** The **ESP32 Main Brain** polls its local physical sensors (DHT22, gated soil moisture, LDR, HC-SR04) and writes a JSON telemetry packet to Firebase every 4 seconds.
* **Rendering:** The app receives the telemetry in under 100ms. It renders live animated dial gauges and begins plotting historical moisture logs in real-time.

### Step 3: Changing a Parameter (Auto Threshold / Manual Override)
* **Action:** The user moves the "Soil Moisture Target" slider on the dashboard to **45%**.
* **Cloud Write:** The Next.js app immediately writes `moisture_threshold = 45` to the `/controls` node of Firebase RTDB.
* **Hardware Pull:** The ESP32 (which is listening to the controls node) reads the updated value.
* **Actuation:** In its loop, the ESP32 compares the current soil moisture (e.g., 38%) against the new target (45%). Since moisture is below the target, the ESP32 flips the **PUMP_RELAY LOW (ON)** and updates `/controls/pump_state = true` in Firebase, which instantly animates the water pump on the user's screen.

### Step 4: On-Demand Camera Scan & AI Diagnostics
* **Action:** The user wants to inspect a leaf. They click the glowing **"Scan Plant Foliage"** button.
* **Trigger:** The app disables further manual clicks, starts a loading spinner, and writes `capture_photo = true` to Firebase.
* **Camera Detection:** The Standalone **ESP32-CAM** (polling Firebase every 2 seconds) reads the true flag.
* **Capture Execution:** The ESP32-CAM turns on its bright white flash LED, captures a single high-res snapshot, and turns the flash OFF immediately to prevent current-draw spikes.
* **Cloud Upload:** The ESP32-CAM posts the raw JPEG bytes to your Vercel serverless endpoint `/api/upload-photo`.
* **Database Updates:**
  1. The server receives the file, uploads it to Firebase Storage, and writes `capture_photo = false` back to Firebase to release the loading spinner.
  2. The server calls the **Plant.id API** to identify leaf spots/diseases.
  3. The server takes those diagnosis results, pings **Gemini 2.0 Flash**, and requests a conversational, monospace-styled remedy text.
  4. The Next.js app renders the leaf photo in its viewport and prints the Gemini AI diagnostic report directly inside the chatbot terminal.
""")

# ----------------------------------------------------
# 6. 03_ESP32_Communication.md
# ----------------------------------------------------
with open("App/03_ESP32_Communication.md", "w") as f:
    f.write("""# 03. ESP32 Communication Protocol

This document details the telemetry, controls, and Wi-Fi reconnection architectures of the **ESP32 DevKit V1** main controller.

---

## 📡 1. Communication Protocols & Transport
All communication between the main controller and the cloud is handled over bidirectionally streamed WebSockets using the **`FirebaseESP32`** library (CP2102 compatible). This completely bypasses slow HTTP REST polling and allows instant, sub-second manual triggers.

---

## 💾 2. Payload Schema Specifications

### A. Sensors Node (Telemetry Output)
Published to the `/sensors` path of your Firebase RTDB every **4 seconds**:

* **JSON Schema:**
```json
{
  "moisture": 52,
  "temperature": 24.5,
  "humidity": 65.0,
  "lux": 800,
  "tank_level": 85
}
```

* **Data Field Validation (Strict Constraints):**
  * `moisture`: Integer, constrained between `0` (bone dry) and `100` (completely saturated).
  * `temperature`: Float, scaled to 1 decimal place.
  * `humidity`: Float, scaled to 1 decimal place.
  * `lux`: Integer, representing raw light levels.
  * `tank_level`: Integer, constrained between `0` (water bucket empty) and `100` (water bucket full), calculated from HC-SR04 ultrasonic distance measurements.

### B. Controls Node (State Input/Output)
Read by the ESP32 continuously over an open WebSocket stream:

* **JSON Schema:**
```json
{
  "manual_mode": false,
  "pump_state": false,
  "grow_light_state": false,
  "moisture_threshold": 40,
  "weather_override": 0
}
```

* **Data Field Definitions:**
  * `manual_mode`: Boolean. If `true`, ESP32 bypasses local automated loops and relies strictly on user toggles. If `false`, ESP32 runs autonomous botanical code.
  * `pump_state`: Boolean. Controls Relay Channel 1.
  * `grow_light_state`: Boolean. Controls the direct 5mm UV LED pin.
  * `moisture_threshold`: Integer (0-100), sets the target soil moisture level.
  * `weather_override`: Integer. If `1`, rain is predicted locally; ESP32 suspends irrigation. If `0`, irrigation is active.

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
# 7. 04_ESP32_CAM_Workflow.md
# ----------------------------------------------------
with open("App/04_ESP32_CAM_Workflow.md", "w") as f:
    f.write("""# 04. ESP32-CAM Vision Node Workflow

This document outlines the on-demand image capture, storage pipeline, and critical network routing configurations of the **ESP32-CAM** standalone vision node.

---

## 📷 1. The On-Demand Camera Loop ("On Appeal")
The ESP32-CAM remains in a low-power, non-streaming idle state. It connects to Wi-Fi and polls the Firebase Realtime Database path `/controls/capture_photo` every 2 seconds.

```
[ Next.js App ]             [ Firebase RTDB ]             [ ESP32-CAM ]             [ Vercel Cloud ]
       │                            │                            │                         │
       │──(Click "Scan")───────────►│                            │                         │
       │                            │(capture_photo = true)      │                         │
       │                            │◄──(Polls capture_photo)────│                         │
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
# 8. 05_Backend_Architecture.md
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
  * If `"rain"`, `"drizzle"`, or `"thunderstorm"` is found, writes `weather_override = 1` to Firebase.
  * If clear, writes `weather_override = 0`.
""")

# ----------------------------------------------------
# 9. 06_Supabase_vs_Firebase.md
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
1. **Processor Overhead & Memory Constraints:** The ESP32 is a low-power microcontroller. Running a SQL-based ORM or assembling complex HTTP POST headers with JWT authorization strings for Supabase's Postgres API uses significant RAM, leading to **heap allocation failures** and crashes. The Mobizt `FirebaseESP32` library operates on highly optimized lightweight JSON parsing and manages SSL/TLS handshakes internally with extreme stability.
2. **Sub-100ms Manual Toggles:** Firebase RTDB holds a persistent, open WebSocket stream with the ESP32. When you click "Force ON" on the app, the state change travels over the air and triggers the pump relay in **less than 100ms**. Supabase’s PostgreSQL real-time engine, while robust, introduces several database layers (Write-Ahead Log listener -> realtime server -> client), resulting in higher latency and slower, clunky physical responses during live demos.
3. **Generous Storage Free Tier:** Firebase offers **5 GB** of cloud storage completely free, which is 5x larger than Supabase's 1 GB free tier. This allows you to store thousands of leaf scans without running out of space!
""")

# ----------------------------------------------------
# 10. 07_Database_Design.md
# ----------------------------------------------------
with open("App/07_Database_Design.md", "w") as f:
    f.write("""# 07. Database Design & Tree Schemas

Since **Firebase Realtime Database** is selected as our core synchronizer, the database is designed as a single, highly optimized, real-time JSON Document Tree.

---

## 🌳 1. Core Document Tree Schema

```json
{
  "verde-tech": {
    "sensors": {
      "moisture": 52,
      "temperature": 24.5,
      "humidity": 65.0,
      "lux": 800,
      "tank_level": 85,
      "last_updated": 1784264500
    },
    "controls": {
      "manual_mode": false,
      "pump_state": false,
      "grow_light_state": false,
      "moisture_threshold": 40,
      "weather_override": 0,
      "capture_photo": false
    },
    "historical_logs": {
      "moisture_log": {
        "1784264500": 52,
        "1784268100": 50
      }
    }
  }
}
```

---

## 📝 2. Field-by-Field Definition

### A. Sensors Node (Telemetry)
* **`moisture` (Integer):** 0 to 100, representing real-time soil moisture percentage from the power-gated sensor.
* **`temperature` (Float):** Ambient temperature in °C from the DHT22.
* **`humidity` (Float):** Ambient air humidity in % from the DHT22.
* **`lux` (Integer):** Ambient light levels in Lux from the LDR.
* **`tank_level` (Integer):** 0 to 100, representing remaining water volume in the bucket from the HC-SR04 ultrasonic sensor.
* **`last_updated` (Long):** Epoch timestamp of the last successful sensor upload.

### B. Controls Node (Configuration & Toggles)
* **`manual_mode` (Boolean):** If `true`, bypasses automatic irrigation code and obeys app toggles. If `false`, runs smart autonomous loops.
* **`pump_state` (Boolean):** State of Relay 1 (Water pump).
* **`grow_light_state` (Boolean):** State of the 5mm UV LED (GPIO 26).
* **`moisture_threshold` (Integer):** User-defined soil target (0-100%) to trigger the water pump in auto-mode.
* **`weather_override` (Integer):** If `1`, local rain predicted; irrigation is suspended. If `0`, active.
* **`capture_photo` (Boolean):** The trigger flag for the ESP32-CAM.

---

## 📈 3. Scalability Expansion Plan
For multi-device deployments (such as managing several distinct pots or greenhouses), nest each system under a unique device MAC address key:
```text
/devices/{device_mac_address}/sensors/...
/devices/{device_mac_address}/controls/...
```
This is fully compatible with NoSQL scaling paradigms.
""")

# ----------------------------------------------------
# 11. 08_API_Design.md
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
# 12. 09_Authentication.md
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
# 13. 10_Row_Level_Security.md
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
    "sensors": {
      // Only authenticated users can read sensor values
      ".read": "auth != null",
      // Only authenticated users/ESP32 can write telemetry
      ".write": "auth != null"
    },
    "controls": {
      ".read": "auth != null",
      // User can change toggles, ESP32 can read
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
# 14. 11_Image_Handling.md
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
# 15. 12_Offline_and_Error_Handling.md
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
* **App Display:** The app sets `/controls/capture_photo = false` in Firebase, stops the user loading spinner, and slides in an error toast: *"❌ Scan Failed: Insufficient power on camera node. Retrying..."*
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
# 16. 13_Notifications.md
# ----------------------------------------------------
with open("App/13_Notifications.md", "w") as f:
    f.write("""# 13. System Notifications & Alarms

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
""")

# ----------------------------------------------------
# 17. 14_UI_UX_Guidelines.md
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
# 18. 15_Project_Rules.md
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
# 19. 16_Best_Practices.md
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
# 20. 17_Future_Improvements.md
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
# 21. 18_Development_Checklist.md
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

print("Successfully compiled and generated all structural files under App/!")
