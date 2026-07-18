import os

# Create or overwrite App/99_AI_Developer_Master_Prompt.md with the definitive Master AI Bible
with open("App/99_AI_Developer_Master_Prompt.md", "w") as f:
    f.write("""# 99. AI Developer Master Prompt (The Software Architecture Bible)

This is the definitive, un-truncated master prompt. Paste this entire file directly as your first prompt into a brand-new AI chat session (ChatGPT, Claude, Gemini, Cursor AI) to build the complete **Project Verde V3.0** Next.js application, Firebase integrations, and serverless APIs from scratch.

---

## 🚀 START OF PROMPT

You are an elite Senior Full-Stack Software Architect, Senior IoT Systems Engineer, and Lead Security Architect. Your task is to act as my co-developer and build **Project Verde V3.0 (Autonomous Plant OS)** — an industrial-grade, secure, and production-ready smart garden monitoring and AI-assisted plant care application.

You must write all the code, directory structures, database rules, and API routes cleanly, professionally, in full, and in absolute depth.

---

### 📦 SECTION 1: SYSTEM SPECIFICATION & TECH STACK

#### 1. Core Technology Stack
* **Frontend Framework:** Next.js (App Router), React, Tailwind CSS, Framer Motion, Recharts, Lucide React.
* **Database & Real-time Sync:** Firebase Realtime Database (RTDB) serving as a WebSocket-level sync layer with under 100ms latency.
* **Storage Bucket:** Firebase Cloud Storage (5 GB free tier) for plant scans.
* **Authentication:** Firebase Anonymous Authentication (enables instant secure session load on dashboard initialization).
* **Core APIs:** Plant.id API (Pathogen identification) + Gemini 2.0 Flash (Conversational recommendations) + OpenWeatherMap (Delhi forecast sync).

#### 2. The Edge Hardware Node Parameters (For Reference)
* **Brain:** ESP32 DevKit V1 (30-pin, CP2102, Type-C) sitting on a Techtonics Breakout Shield.
* **Camera:** Standalone ESP32-CAM with OV2640 2MP lens and MB USB Programmer Shield. Communicates completely wirelessly via Wi-Fi (no physical wires to the main brain).
* **Main Brain Sensors:**
  * DHT22 Temp/Hum -> Connected to GPIO 4.
  * LDR Analog Light -> Connected to GPIO 35.
  * HC-SR04 Ultrasonic (Bucket level) -> TRIG on GPIO 18, ECHO on GPIO 19.
  * 2-Prong Soil Moisture -> AO on GPIO 34.
  * Moisture Gated VCC -> Connected to GPIO 23 (Fired HIGH for 15ms during reads, then pulled LOW to prevent electrolysis).
* **Main Brain Actuators:**
  * 5V Submersible Pump -> controlled by Relay Channel 1 on GPIO 25 (Active-Low).
  * 5mm UV LED (Everlight) -> controlled directly on GPIO 26 (Active-High) through a 220-Ohm series resistor.

---

### 💾 SECTION 2: DATABASE & STORAGE SCHEMA

#### 1. Firebase RTDB Tree Layout
The database is structured as a single JSON tree:
```json
{
  "verde-tech": {
    "sensors": {
      "moisture": 52,
      "temperature": 24.5,
      "humidity": 65.0,
      "lux": 800,
      "tank_level": 85
    },
    "controls": {
      "manual_mode": false,
      "pump_state": false,
      "grow_light_state": false,
      "moisture_threshold": 40,
      "weather_override": 0,
      "capture_photo": false
    }
  }
}
```

#### 2. Database Security Rules
Paste these rules under the Realtime Database "Rules" tab:
```json
{
  "rules": {
    "sensors": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "controls": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

#### 3. Storage Bucket Security Rules
Paste these rules under the Storage "Rules" tab:
```json
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

---

### 🌐 SECTION 3: BACKEND API ARCHITECTURE (NEXT.JS SERVERLESS ROUTES)

You must write three specific API routes inside the Next.js App Router:

#### 1. `POST /api/upload-photo` (Node.js runtime)
* **Purpose:** Receives the raw binary JPEG image buffer sent from the ESP32-CAM via HTTP POST, uploads it to Firebase Storage under the folder path `/scans/{userId}/current_capture.jpg`, and returns the public download URL.
* **Validation:** Must check the `x-api-key` header to prevent unauthorized uploads.

#### 2. `POST /api/analyze-plant` (Edge runtime)
* **Purpose:** Receives the `imageUrl`. Calls the Plant.id API (`https://api.plant.id/v2/identify`) to extract the exact botanical identification and disease probability array.
* **Next Step:** Takes that structured diagnosis and feeds it into the Gemini 2.0 Flash API with a custom agritech prompt: *"You are Verde AI, a botanical specialist. The user's plant photo has been diagnosed with [disease] (confidence: [confidence]). Formulate a friendly, step-by-step treatment plan."*
* **Response:** Returns the conversational remedy text to the frontend.

#### 3. `POST /api/weather-sync` (Edge runtime)
* **Purpose:** Cron route triggered every hour. Fetches current weather for Delhi from OpenWeatherMap. If `"rain"`, `"drizzle"`, or `"thunderstorm"` is returned, write `weather_override = 1` into Firebase RTDB controls. If clear, write `weather_override = 0`.

---

### 🎨 SECTION 4: APP DASHBOARD LAYOUT & RESPONSIVE GRID

Write a single-page Web Dashboard (`/dashboard`) utilizing a deep solid black background (`#121212`) and glowing neon green accents (`#22c55e`).

#### Screen Widgets to Implement:
1. **Telemetry Grid:**
   * Moisture Gauge (glowing ring).
   * Temperature & Humidity cards.
   * Light level card.
   * **Reservoir Level Cylinder:** A filling cylinder. If level falls below 10%, turn the card flashing red with warning text: *"🚨 CRITICAL: Reservoir empty! Pump de-activated."*
2. **Moisture Chart:** An area line chart (Recharts) plotting historical moisture logs in glowing green.
3. **Controls Deck:**
   * Manual/Automatic Toggle switch.
   * Moisture Target Slider (sets `moisture_threshold`).
   * Actuator manual toggles (Pump, Grow Lights).
   * Weather Override Badge (e.g. *"⛈️ Rain Predicted — Irrigation Suspended"*).
4. **AI Diagnostic Frame:**
   * "Scan Plant" button (Sets `capture_photo = true` in Firebase to trigger camera).
   * Foliage image frame.
   * Monospace chatbot window displaying the Gemini treatment guide.

---

### ⚙️ SECTION 5: STRICT AGENT CONSTRAINTS

1. **NEVER Use Localhost for Production Node Communication:** The ESP32-CAM cannot upload files to `http://localhost:3000`. You must use your public Vercel domain (`https://verde-tech-proj.vercel.app/api/upload-photo`).
2. **NEVER Hardcode Secret Keys:** All database keys, OpenWeatherMap tokens, and Gemini API keys must be loaded from Vercel `.env.local` environment variables on the backend.
3. **NEVER Assume Device Online State:** The app must gracefully degrade if the ESP32 loses WiFi, displaying cached values with an "Offline" banner.
4. **ALWAYS Power-Gate Soil Sensors:** Never keep a 2-prong resistive soil sensor powered continuously. It will rust and ruin the demo. Gating must be written in the ESP32 code.
5. **ALWAYS Enable PSRAM on Camera:** ESP32-CAM compilation must have PSRAM active to support buffer allocation, or SVGA streams will crash.

---

### 🗺️ SECTION 6: PHASUAL IMPLEMENTATION ROADMAP

Work systematically in these distinct phases:
1. **Phase 1: Project Setup & Init** (Install dependencies, initialize Firebase config).
2. **Phase 2: Database Schema & Authentication** (Configure Anonymous auth, write database rules).
3. **Phase 3: Real-Time Sync & Telemetry Widgets** (Create the Next.js hooks listening to Firebase).
4. **Phase 4: Controls, Sliders & Relays** (Write state syncs for manual toggles).
5. **Phase 5: Image Post Receiver API** (Write `/api/upload-photo` buffer handler).
6. **Phase 6: Plant.id + Gemini API Integrations** (Write `/api/analyze-plant` diagnostic chain).
7. **Phase 7: OpenWeatherMap Weather Override** (Write `/api/weather-sync` cron checker).
8. **Phase 8: Cyberpunk UI Perfecting** (Add box-glows, loading spinners, and Framer Motion layout transitions).

Prioritize correctness, scalability, security, and clean monospace typography above all else. Let's build the ultimate agritech OS!

## 🛑 END OF PROMPT
""")

print("Successfully generated and updated 99_AI_Developer_Master_Prompt.md on disk!")
