import os

# Create App directory
os.makedirs("App", exist_ok=True)

# ----------------------------------------------------
# 1. README.md
# ----------------------------------------------------
with open("App/README.md", "w") as f:
    f.write("""# Verde Tech V3.0 — Developer Handoff Documentation

Welcome to the official developer handoff documentation folder for **Project Verde V3.0 (Autonomous Plant OS)**. This folder contains the complete technical specifications, database architectures, and API designs required to build the web and mobile applications from scratch.

## 📂 Documentation Directory

1. **[00_Project_Overview.md](./00_Project_Overview.md):** Project goals, target users, and components.
2. **[01_System_Architecture.md](./01_System_Architecture.md):** High-level topology and block diagrams.
3. **[02_Application_Workflow.md](./02_Application_Workflow.md):** Step-by-step user-to-device workflows.
4. **[03_ESP32_Communication.md](./03_ESP32_Communication.md):** Telemetry payload specs and Wi-Fi reconnection models.
5. **[04_ESP32_CAM_Workflow.md](./04_ESP32_CAM_Workflow.md):** On-demand image capture, storage pipelines, and production routing.
6. **[05_Backend_Architecture.md](./05_Backend_Architecture.md):** Node.js/Next.js serverless route configuration.
7. **[06_Supabase_vs_Firebase.md](./06_Supabase_vs_Firebase.md):** Direct comparison and final architecture recommendation.
8. **[07_Database_Design.md](./07_Database_Design.md):** Schema design, index strategies, and document trees.
9. **[08_API_Design.md](./08_API_Design.md):** Full REST endpoint specifications and payload examples.
10. **[09_Authentication.md](./09_Authentication.md):** Sign-up, login, and session lifecycles.
11. **[10_Row_Level_Security.md](./10_Row_Level_Security.md):** Security policies and bucket permission rules.
12. **[11_Image_Handling.md](./11_Image_Handling.md):** Image compression, storage, and 15-day auto-delete TTL policies.
13. **[12_Offline_and_Error_Handling.md](./12_Offline_and_Error_Handling.md):** Hard-fault, network drop, and device offline recovery.
14. **[13_Notifications.md](./13_Notifications.md):** Alerts, push frameworks, and dry-run pump warnings.
15. **[14_UI_UX_Guidelines.md](./14_UI_UX_Guidelines.md):** UI theme, loading states, grids, and accessibility.
16. **[15_Project_Rules.md](./15_Project_Rules.md):** Strict constraints (no localhost, no exposed keys, secure envs).
17. **[16_Best_Practices.md](./16_Best_Practices.md):** Directory structure, naming conventions, and testing strategies.
18. **[17_Future_Improvements.md](./17_Future_Improvements.md):** AI crop matching, weather routing, and predictive analytics.
19. **[18_Development_Checklist.md](./18_Development_Checklist.md):** Modular, step-by-step developer implementation tasks.
20. **[99_AI_Developer_Master_Prompt.md](./99_AI_Developer_Master_Prompt.md):** The master bootstrap prompt to feed a brand-new AI session.

---

## 🛠️ Tech Stack Baseline
* **Frontend:** Next.js (App Router), Tailwind CSS, Framer Motion, Recharts.
* **Backend:** Next.js Serverless API Routes (Node.js runtimes).
* **Database/Sync:** Firebase Realtime Database (WebSocket sync).
* **Storage:** Firebase Cloud Storage (5GB Free tier, 15-Day TTL).
* **AI:** Plant.id API (Diagnosis) + Gemini 2.0 Flash API (Conversational Advisor).
""")

# ----------------------------------------------------
# 2. 00_Project_Overview.md
# ----------------------------------------------------
with open("App/00_Project_Overview.md", "w") as f:
    f.write("""# 00. Project Overview

## Goal
To build a production-ready, low-cost agritech system for residential gardening and precision farming. Enables remote, automated, and AI-assisted plant care from anywhere.

## Target Users
* Home gardeners managing plants while away.
* Hobbyists monitoring soil nutrients and plant hydration.
* Small-scale greenhouse operators needing automated growth lights and irrigation.

## System Components
1. **The Edge Controller:** Single ESP32 DevKit V1 with G-V-S expansion board.
2. **The Vision Node:** Independent ESP32-CAM with MB Programmer Shield.
3. **The Web Dashboard:** Next.js (Tailwind + Recharts) hosted on Vercel.
4. **The Real-Time Bridge:** Firebase Realtime Database.
5. **The AI Core:** Plant.id + Gemini 2.0 Flash.

## Technical Baseline
* **Database latency:** <100ms.
* **Watering safety:** Automatic deactivation if reservoir falls below 10%.
* **Power consumption:** <400mA continuous (powered via stable 5V USB connection).
""")

# ----------------------------------------------------
# 3. 01_System_Architecture.md
# ----------------------------------------------------
with open("App/01_System_Architecture.md", "w") as f:
    f.write("""# 01. System Architecture

## Overview
The system follows a decoupled, headless, event-driven IoT design. Hardware devices do not talk directly to the web client. Instead, they sync state over WebSockets with the database.

## System Topology
```
 [ Next.js Web Client ] <=======(WebSockets)=======> [ Firebase RTDB ]
          │                                                  ▲
 (HTTP POST)                                                 │
          ▼                                            (WiFi Sync)
 [ Next.js API Routes ]                                      ▼
   (Vercel Cloud)                                   [ ESP32 Main Brain ]
          │                                        (Sensors & Relays)
    (REST Requests)
          ▼
 [ External AI APIs ] (Plant.id / Gemini)
```

## System Boundaries
* **The Local AP Network:** ESP32-CAM hosts local SoftAP (`Verde-Tech-Cam`) at `192.168.4.1` for standalone web server tests.
* **The Internet Mesh:** In production, both the ESP32 and ESP32-CAM connect over WiFi to the user's mobile hotspot/router. All state synchronizes through Firebase RTDB.
""")

# ----------------------------------------------------
# 4. 02_Application_Workflow.md
# ----------------------------------------------------
with open("App/02_Application_Workflow.md", "w") as f:
    f.write("""# 02. Application Workflow

## Main End-to-End Sequence

```
User App                  Firebase RTDB                 ESP32 Brain             ESP32-CAM
  │                            │                             │                       │
  │───(Loads Dashboard)───────►│                             │                       │
  │                            │◄──(Streams Telemetry)───────│                       │
  │◄──(Renders live data)──────│                             │                       │
  │                            │                             │                       │
  │───(Clicks "Scan Leaf")────►│(capture_photo = true)       │                       │
  │                            │                             │                       │
  │                            │◄──(Polls capture flag)──────┼───────────────────────│
  │                            │                             │                       │
  │                            │                             │──(Flashes & Snaps)───►│
  │                            │                             │                       │
  │◄──(POSTs raw JPEG image)───┼─────────────────────────────┼───────────────────────│
  │                            │                             │                       │
  │───(Resets capture flag)───►│(capture_photo = false)      │                       │
  │                            │                             │                       │
  │───(Runs Plant.id & Gemini)─►│                             │                       │
  │                            │                             │                       │
  │◄──(Renders AI Analysis)────│                             │                       │
```

## Steps
1. **Dashboard Initialization:** Next.js loads and opens a real-time listener to Firebase `/sensors` and `/controls`.
2. **Telemetry Stream:** ESP32 reads soil moisture, temperature, humidity, light, and tank level, posting updates every 4 seconds.
3. **Capture Trigger:** Clicking "Scan Foliage" toggles `/controls/capture_photo = true` in Firebase.
4. **Camera Activation:** ESP32-CAM reads the true flag, fires its flash, takes a snapshot, and POSTs the raw binary bytes to the Next.js API.
5. **Flag Reset:** Next.js resets `/controls/capture_photo = false` to release the UI spinner.
6. **AI Diagnostics:** The Next.js backend forwards the image to Plant.id, gets the disease list, queries Gemini 2.0 for treatment steps, and displays them.
""")

# ----------------------------------------------------
# 5. 03_ESP32_Communication.md
# ----------------------------------------------------
with open("App/03_ESP32_Communication.md", "w") as f:
    f.write("""# 03. ESP32 Communication Protocol

## Protocol
Communication is entirely bidirectionally managed over WebSockets via the `Firebase-ESP32` library.

## Telemetry Payload Structure
Sent to `/sensors` every 4 seconds:
```json
{
  "moisture": 52,
  "temperature": 24.5,
  "humidity": 65.0,
  "lux": 800,
  "tank_level": 85
}
```

## Controls Payload Structure
Read by ESP32 continuously:
```json
{
  "manual_mode": false,
  "pump_state": false,
  "grow_light_state": false,
  "moisture_threshold": 40,
  "weather_override": 0
}
```

## Reconnection Logic
If Wi-Fi drops, the ESP32 must run non-blocking reconnection attempts:
```cpp
if (WiFi.status() != WL_CONNECTED) {
  unsigned long currentMillis = millis();
  if (currentMillis - lastRetry > 5000) {
    lastRetry = currentMillis;
    WiFi.disconnect();
    WiFi.begin(ssid, password);
  }
}
```
* **No Blocking:** This allows the physical board to continue checking hardware thresholds even if Wi-Fi is temporarily lost.
""")

# ----------------------------------------------------
# 6. 04_ESP32_CAM_Workflow.md
# ----------------------------------------------------
with open("App/04_ESP32_CAM_Workflow.md", "w") as f:
    f.write("""# 04. ESP32-CAM Workflow

## The "On Appeal" Architecture
The ESP32-CAM remains in an idle state. It connects to Wi-Fi, polls Firebase `/controls/capture_photo` every 2 seconds, and fires only on demand.

## Connection & Payload
```cpp
HTTPClient http;
http.begin("https://verde-tech-proj.vercel.app/api/upload-photo");
http.addHeader("Content-Type", "image/jpeg");
int httpResponseCode = http.POST(fb->buf, fb->len);
```

## Why Localhost is Bad
The ESP32-CAM is an independent physical network node.
* **The Error:** Directing the camera to `http://localhost:3000/api/upload-photo` fails. `localhost` refers to the camera board itself!
* **The Production Fix:** The camera must always route packets to the public Next.js domain (`https://verde-tech-proj.vercel.app/api/upload-photo`) or, for local testing, the laptop's exact local hotspot IP address (`http://192.168.1.6:5000/upload`).

## Advantages of Recommended Architecture
* **Saves Power:** Camera lens and flash run only for 1 second during capture.
* **No SD Card Errors:** Images are saved in 4MB internal PSRAM (Frame Buffer) and streamed directly over WiFi. This prevents slow SD-card read/write delays and mounting faults.
""")

# ----------------------------------------------------
# 7. 05_Backend_Architecture.md
# ----------------------------------------------------
with open("App/05_Backend_Architecture.md", "w") as f:
    f.write("""# 05. Backend Architecture

## Overview
Next.js serverless API routes handle heavy computation, third-party authentication, external API calls, and asset uploads.

## API Runtimes
Next.js Edge Runtimes are used for quick API execution, while standard Node.js runtimes are used for raw image processing and binary buffer manipulation.

## Core Endpoints
1. `/api/upload-photo` (Node.js runtime): Receives binary JPEG buffers from the ESP32-CAM and writes them to Firebase Storage.
2. `/api/analyze-plant` (Edge runtime): Handshakes with Plant.id and Gemini APIs.
3. `/api/weather-sync` (Edge runtime): Fetches OpenWeatherMap API and updates `weather_override` in Firebase RTDB.

## Security Controls
All backend API routes must validate request headers. Standard uploads require an `x-api-key` header to prevent arbitrary image spamming to your storage buckets.
""")

# ----------------------------------------------------
# 8. 06_Supabase_vs_Firebase.md
# ----------------------------------------------------
with open("App/06_Supabase_vs_Firebase.md", "w") as f:
    f.write("""# 06. Supabase vs. Firebase Comparison

## Detailed Evaluation

| Feature | Firebase (RTDB) | Supabase (PostgreSQL) |
| :--- | :--- | :--- |
| **Real-Time Sync** | WebSocket streaming natively (<100ms). | Polling / Realtime triggers on Postgres. |
| **Microcontroller Libs**| Extremely stable `Firebase-ESP32` client. | Complex manual REST/JWT handling. |
| **Storage** | 5 GB free tier, robust SDKs. | 1 GB free tier. |
| **Auth** | Instant, simple anonymous/email auth. | Postgres GoTrue integration. |
| **Ease of Build** | Super-fast JSON-tree sync. | Requires structured schema migrations. |

## Recommendation
**Firebase Realtime Database (RTDB) is selected as the production database.**
* **Why:** Real-time sync on microcontrollers must be extremely lightweight. The Mobizt `FirebaseESP32` client handles SSL and WebSockets internally. Running a SQL-based ORM or raw HTTP client on an ESP32 is memory-heavy, slow, and prone to heap crashes.
""")

# ----------------------------------------------------
# 9. 07_Database_Design.md
# ----------------------------------------------------
with open("App/07_Database_Design.md", "w") as f:
    f.write("""# 07. Database Design

## Database Type: Firebase Realtime Database
Since we are using Firebase RTDB, the database is structured as a single JSON tree.

## Document Schema Design
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

## Scale Plan
For multi-device deployments, nest devices under unique device MAC-address keys:
`/devices/{device_mac}/sensors`
""")

# ----------------------------------------------------
# 10. 08_API_Design.md
# ----------------------------------------------------
with open("App/08_API_Design.md", "w") as f:
    f.write("""# 08. API Design

## Endpoints Specification

### 1. Upload Photo
* **Endpoint:** `POST /api/upload-photo`
* **Headers:** `Content-Type: image/jpeg`, `x-device-id: verde-cam-1`
* **Request Body:** Raw binary JPEG image buffer.
* **Success Response (200):**
```json
{
  "success": true,
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/..."
}
```

### 2. Analyze Plant
* **Endpoint:** `POST /api/analyze-plant`
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/..."
}
```
* **Success Response (200):**
```json
{
  "plant_identified": "Ocimum tenuiflorum (Tulsi)",
  "health_diagnosis": "Mild leaf spots detected",
  "gemini_remedy": "Add organic compost and reduce watering moisture threshold to 40%."
}
```
""")

# ----------------------------------------------------
# 11. 09_Authentication.md
# ----------------------------------------------------
with open("App/09_Authentication.md", "w") as f:
    f.write("""# 09. Authentication

## Strategy
For a local exhibition prototype (DAV ACON 5), the app must load instantly without registration delays, but still protect database writes.

## Implementation: Firebase Anonymous Authentication
* **Why:** Allows the dashboard to create a secure, authenticated session for the web browser in milliseconds without typing passwords.
* **Implementation:**
```javascript
import { getAuth, signInAnonymously } from "firebase/auth";

const auth = getAuth();
signInAnonymously(auth)
  .then(() => {
    console.log("Secure Anonymous Session Initialized!");
  })
  .catch((error) => {
    console.error("Auth failed:", error);
  });
```

## Session Storage
Tokens are automatically cached in `IndexedDB` by the Firebase Web SDK, providing persistent sessions across browser reloads.
""")

# ----------------------------------------------------
# 12. 10_Row_Level_Security.md
# ----------------------------------------------------
with open("App/10_Row_Level_Security.md", "w") as f:
    f.write("""# 10. Security & Database Rules

## Firebase Security Rules
To secure your real-time database while allowing your ESP32 boards (which use a simple Database Secret key) and your anonymous app users to write, use these production rules:

```javascript
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

## Storage Bucket Security Rules
Ensure only authenticated sessions can write plant scans, but public URLs can render them on your app:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      allow read: if true; // Publicly readable for dashboard rendering
      allow write: if request.auth != null; // Only authenticated users/APIs can write
    }
  }
}
```
""")

# ----------------------------------------------------
# 13. 11_Image_Handling.md
# ----------------------------------------------------
with open("App/11_Image_Handling.md", "w") as f:
    f.write("""# 11. Image Handling Pipeline

## Upload and Compression
1. **At ESP32-CAM:** Camera captures at `SVGA (800x600)` to keep image size small (~60 KB) and prevent memory fragmentation.
2. **At Next.js Server:** Next.js receives the raw binary buffer and streams it straight to Firebase Storage under the folder: `/scans/{userId}/current_capture.jpg`.

## 15-Day Auto-Delete Policy (TTL)
To prevent your 5GB free storage tier from filling up, implement a serverless Node.js lifecycle cleanup routine:

```javascript
// Next.js Cron Route: /api/cleanup-storage
import { getStorage } from "firebase-admin/storage";

export default async function handler(req, res) {
  const bucket = getStorage().bucket();
  const [files] = await bucket.getFiles({ prefix: "scans/" });
  
  const fifteenDaysAgo = Date.now() - (15 * 24 * 60 * 60 * 1000);
  
  for (const file of files) {
    const [metadata] = await file.getMetadata();
    const createdTime = new Date(metadata.timeCreated).getTime();
    
    if (createdTime < fifteenDaysAgo) {
      await file.delete();
      console.log(`Deleted stale image scan: ${file.name}`);
    }
  }
  res.status(200).json({ success: true });
}
```
""")

# ----------------------------------------------------
# 14. 12_Offline_and_Error_Handling.md
# ----------------------------------------------------
with open("App/12_Offline_and_Error_Handling.md", "w") as f:
    f.write("""# 12. Offline & Error Handling

## Hard Fault States and Recovery

### 1. ESP32 Main Brain Offline
* **App Display:** The web dashboard detects that the database `last_updated` timestamp is older than 10 seconds. It displays a red glowing badge: *"⚠️ EDGE OFFLINE: System operating autonomously"*.
* **Recovery:** The ESP32 loop runs independent threshold routines. If moisture falls below target, it still waters locally, ensuring survival even without WiFi!

### 2. Wi-Fi Connection Loss
* **App Display:** App keeps displaying cached values in Firebase and marks the device as offline.
* **Recovery:** ESP32 uses non-blocking retry tasks (`WiFi.begin()`) every 5 seconds without freezing.

### 3. Image Capture Failure
* **App Display:** If the ESP32-CAM fails to take a picture (brownout or lens loose), the Next.js API times out. The app resets the capture flag and displays: *"❌ Scan Failed: Check camera connections and power."*
""")

# ----------------------------------------------------
# 15. 13_Notifications.md
# ----------------------------------------------------
with open("App/13_Notifications.md", "w") as f:
    f.write("""# 13. System Notifications

## Notification Types

### 1. Reservoir Low Warning (Critical)
* **Trigger:** HC-SR04 reads water level <10%.
* **Behavior:** Turn the dashboard bucket cylinder bright flashing red and display a persistent banner: *"🚨 CRITICAL: Water Reservoir Empty! Pump deactivated to prevent motor damage."*

### 2. Smart Weather Suspension
* **Trigger:** Weather forecast API returns rain.
* **Behavior:** Display a pulsing green banner: *"⛈️ Weather Sync: Watering suspended. Rain forecasted in Delhi today. Saving water!"*

### 3. Growth light activation
* **Trigger:** Lux sensor < 400.
* **Behavior:** Slide in a temporary toast notification: *"☀️ Low Light Detected: Photosynthetic LED array turned on."*
""")

# ----------------------------------------------------
# 16. 14_UI_UX_Guidelines.md
# ----------------------------------------------------
with open("App/14_UI_UX_Guidelines.md", "w") as f:
    f.write("""# 14. UI/UX Guidelines

## Visual Theme: Verde Cyberpunk
* **Backgrounds:** Deep solid blacks (`#000000`, `#121212`) and high-tech dark grays (`#1a1a1a`).
* **Accents:** Neon botanical green (`#22c55e`, `rgb(34,197,94)`).
* **Text:** Glowing green monospace fonts (`Courier Prime`, `Share Tech Mono`).

## Core Screens
1. **Console Deck (Dashboard):**
   * Top bar: Firebase connection state, Delhi weather badge.
   * Left: Live telemetry gauges (Moisture, Temp, Humidity, Reservoir Level).
   * Center: Real-time Recharts line graph plotting moisture.
   * Right: Actuator toggles (Manual/Auto switches) and threshold slider.
2. **AI Botanist Panel:**
   * Bottom half of the screen. Holds the "Scan Foliage" capture button, image frame viewport, and a chat window displaying Gemini 2.0 leaf health diagnostics.

## Interactive States
* **Hover States:** Hovering over cards must trigger a subtle green glow (`box-shadow: 0 0 15px rgba(34,197,94,0.3)`).
* **Loading States:** Clicking "Scan" turns the button into a spinning progress loader and disables manual clicks until Firebase resets.
""")

# ----------------------------------------------------
# 17. 15_Project_Rules.md
# ----------------------------------------------------
with open("App/15_Project_Rules.md", "w") as f:
    f.write("""# 15. Project Rules

## Absolute Constraints for Developers

1. **NEVER Use Localhost in Production:** The ESP32-CAM cannot upload files to `http://localhost:3000`. You must use your public Vercel domain (`https://verde-tech-proj.vercel.app/api/upload-photo`).
2. **NEVER Hardcode Secret Keys:** All database keys, OpenWeatherMap tokens, and Gemini API keys must be loaded from Vercel `.env.local` environment variables on the backend.
3. **NEVER Assume Device Online State:** The app must gracefully degrade if the ESP32 loses WiFi, displaying cached values with an "Offline" banner.
4. **ALWAYS Power-Gate Soil Sensors:** Never keep a 2-prong resistive soil sensor powered continuously. It will rust and ruin the demo. Gating must be written in the ESP32 code.
5. **ALWAYS Enable PSRAM on Camera:** ESP32-CAM compilation must have PSRAM active to support buffer allocation, or SVGA streams will crash.
""")

# ----------------------------------------------------
# 18. 16_Best_Practices.md
# ----------------------------------------------------
with open("App/16_Best_Practices.md", "w") as f:
    f.write("""# 16. Best Practices

## Directory Structure
```text
next-app/
├── app/
│   ├── api/
│   │   ├── upload-photo/   # Camera upload receiver (Node.js)
│   │   ├── analyze-plant/  # Plant.id + Gemini API route (Edge)
│   │   └── weather-sync/   # OpenWeatherMap fetch route (Edge)
│   ├── dashboard/          # Next.js main web client
│   └── page.js             # Landing splash screen
├── components/             # Reusable UI widgets
├── lib/
│   └── firebase.js         # Firebase initialized client
└── public/                 # Static assets
```

## Security
* Sanitize all REST payloads on Vercel backend routes before querying the database.
* Keep Firebase database rules strict: no public write access without authentication tokens.

## Maintainability
* Comment every function.
* Handle API errors gracefully using try/catch structures, returning clean 500 error responses to the frontend.
""")

# ----------------------------------------------------
# 17. 17_Future_Improvements.md
# ----------------------------------------------------
with open("App/17_Future_Improvements.md", "w") as f:
    f.write("""# 17. Future Improvements

## Scalability Roadmap

1. **Predictive Analytics:** Train a lightweight TensorFlow model to study soil moisture depletion curves over time, predicting *exactly* how many hours are left before the next irrigation cycle is needed.
2. **Multi-Farm Clusters:** Upgrade the database tree schema to support multiple MAC addresses, allowing a single dashboard user to toggle between several greenhouses or residential gardens.
3. **Smart Nutrient Recommendation:** Integrate direct Soil pH and true RS485 NPK probes to automate NPK depletion reporting and fertilizing schedules.
""")

# ----------------------------------------------------
# 18. 18_Development_Checklist.md
# ----------------------------------------------------
with open("App/18_Development_Checklist.md", "w") as f:
    f.write("""# 18. Development Checklist

## Phase 1: Firebase Project Setup
* [ ] Create a new project on Firebase Console.
* [ ] Initialize a **Realtime Database** in Test Mode.
* [ ] Enable **Firebase Storage** (default bucket).
* [ ] Enable **Anonymous Authentication** in the Auth tab.
* [ ] Save credentials and database URL as environment variables.

## Phase 2: Next.js Frontend Foundation
* [ ] Bootstrap the Next.js project with `npx create-next-app@latest`.
* [ ] Install `firebase`, `recharts`, `framer-motion`, and `lucide-react`.
* [ ] Build the layout skeleton: monospace styling with dark-mode black background.
* [ ] Set up Firebase WebSocket listeners to feed state variables into React `useState` hooks.

## Phase 3: Actuators, Graphs & Override Logic
* [ ] Build the real-time Moisture chart using Recharts `AreaChart`.
* [ ] Code the Auto/Manual mode toggle buttons.
* [ ] Create the target threshold slider.
* [ ] Code the manual Pump and Grow Light force-trigger buttons.

## Phase 4: API Endpoints & AI Setup
* [ ] Write the `/api/upload-photo` Node.js route.
* [ ] Write the `/api/analyze-plant` route (fetching Plant.id & Gemini).
* [ ] Write the `/api/weather-sync` OpenWeatherMap fetcher.
* [ ] Connect the AI results into the conversational chat UI frame.
""")

# ----------------------------------------------------
# 21. 99_AI_Developer_Master_Prompt.md
# ----------------------------------------------------
with open("App/99_AI_Developer_Master_Prompt.md", "w") as f:
    f.write("""# 99. AI Developer Master Prompt

This is the definitive, un-truncated master prompt. Paste this entire prompt into a brand-new AI chat session (ChatGPT, Claude, Gemini, Cursor AI) to build the complete Project Verde V3.0 Next.js application from scratch with zero ambiguity.

---

## 🚀 START OF PROMPT

You are an elite Senior Full-Stack Software Architect, Senior IoT Engineer, and Security Lead. Your task is to build **Project Verde V3.0 (Autonomous Plant OS)** — a production-ready smart garden monitoring and AI-assisted plant care application. 

You must write all the code, directory architectures, database integrations, and API routes cleanly, professionally, and in absolute depth.

---

### 📦 SECTION 1: SYSTEM SPECIFICATION

#### 1. Tech Stack Requirements
* **Frontend Framework:** Next.js (App Router), React, Tailwind CSS, Recharts, Framer Motion, Lucide React.
* **Database & real-time sync:** Firebase Realtime Database (RTDB).
* **Storage bucket:** Firebase Cloud Storage (5 GB free tier) for plant scans.
* **Authentication:** Firebase Anonymous Authentication (allows instant secure session load).
* **Core APIs:** Plant.id (Botanical diagnosis) + Gemini 2.0 Flash (Conversational recommendations) + OpenWeatherMap (Predictive watering override).

#### 2. The Edge Hardware Node Parameters
* **Brain:** ESP32 WROOM-32 30-Pin Board sitting on a Techtonics Breakout Expansion Shield.
* **Camera:** ESP32-CAM OV2640 with an MB USB Programmer Shield.
* **Telemetry interval:** Reads and posts values to Firebase RTDB every 4 seconds.
* **Communication:** Connected wirelessly to the user's Wi-Fi hotspot.
* **Relay:** Robocraze 5V Dual-Channel Relay (Channel 1: 5V Pump, Channel 2: Spare).
* **LED:** Everlight 5mm UV LED driven directly by ESP32 GPIO 26.

---

### 🔌 SECTION 2: HARDWARE CONNECTIONS (FOR REFERENCE)
All sensors are wired directly to the G-V-S rows of the ESP32 shield:
* **DHT22 Temp/Hum:** G-V-S Port 4.
* **Capacitive Moisture:** G-V-S Port 34.
* **Moisture Gated VCC:** G-V-S Port 23 (Fired HIGH for 15ms during reads, then pulled LOW to prevent corrosion).
* **LDR Light:** G-V-S Port 35.
* **HC-SR04 Ultrasonic (Bucket level):** TRIGGER on Port 18, ECHO on Port 19.
* **Robocraze Relay:** IN1 on Port 25 (Pump).
* **5mm UV LED:** S on Port 26 (with 220-Ohm series resistor).

---

### 💾 SECTION 3: DATABASE & STORAGE DESIGN

#### 1. Firebase RTDB Tree
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

#### 2. Security Rules
* **Database Rules:** Allow read/write access to authenticated sessions (`auth != null`).
* **Storage Rules:** Allow read access publicly, but restrict writes strictly to authenticated API routes.

---

### 🌐 SECTION 4: BACKEND API ARCHITECTURE (NEXT.JS SERVERLESS ROUTES)

You must write three specific API routes inside the Next.js App Router:

#### 1. `POST /api/upload-photo` (Node.js runtime)
* **Behavior:** Receives the raw binary JPEG image buffer sent from the ESP32-CAM, uploads it to Firebase Storage under the folder path `/scans/{userId}/current_capture.jpg`, and returns the public download URL.
* **Validation:** Must check the `x-api-key` header to prevent arbitrary buffer uploads.

#### 2. `POST /api/analyze-plant` (Edge runtime)
* **Behavior:** Receives the `imageUrl`. Calls the Plant.id API (`https://api.plant.id/v2/identify`) to extract the exact botanical identification and disease probability array.
* **Next Step:** Takes that structured diagnosis and feeds it into the Gemini 2.0 Flash API with a custom agritech prompt: *"You are Verde AI, a botanical specialist. The user's plant photo has been diagnosed with [disease] (confidence: [confidence]). Formulate a friendly, step-by-step treatment plan."*
* **Response:** Returns the conversational remedy text to the frontend.

#### 3. `POST /api/weather-sync` (Edge runtime)
* **Behavior:** Cron route triggered every hour. Fetches current weather for Delhi from OpenWeatherMap. If `"rain"`, `"drizzle"`, or `"thunderstorm"` is returned, write `weather_override = 1` into Firebase RTDBcontrols. If clear, write `weather_override = 0`.

---

### 🎨 SECTION 5: APP SCREEN LAYOUT (CYBERPUNK BOTANICAL ACCENTS)

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
   * Weather Override Badge (e.g. *"⛈️ Rain Predicted: Irrigation Suspended"*).
4. **AI Diagnostic Frame:**
   * "Scan Plant" button (Sets `capture_photo = true` in Firebase to trigger camera).
   * Foliage image frame.
   * Monospace chatbot window displaying the Gemini treatment guide.

---

### 🚀 SECTION 6: EXECUTION WORKFLOW FOR THE AI

Work systematically in these distinct phases:
1. **Phase 1: Project Setup & Init** (Install dependencies, initialize Firebase config).
2. **Phase 2: Database Schema & Authentication** (Configure Anonymous auth, write database rules).
3. **Phase 3: Real-Time Sync & Telemetry Widgets** (Create the Next.js hooks listening to Firebase).
4. **Phase 4: Controls, Sliders & Relays** (Write state syncs for manual toggles).
5. **Phase 5: Image Post Receiver API** (Write `/api/upload-photo` buffer handler).
6. **Phase 7: Plant.id + Gemini API Integrations** (Write `/api/analyze-plant` diagnostic chain).
7. **Phase 8: OpenWeatherMap Weather Override** (Write `/api/weather-sync` cron checker).
8. **Phase 9: Cyberpunk UI Perfecting** (Add box-glows, loading spinners, and Framer Motion layout transitions).

Prioritize correctness, scalability, security, and clean monospace typography above all else. Let's build the ultimate agritech OS!

## 🛑 END OF PROMPT
""")

print("Successfully written all handoff documentation files under /home/user/App/!")
