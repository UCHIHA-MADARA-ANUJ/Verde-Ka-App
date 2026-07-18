# 02. Complete Application Workflow & Logical Sequences

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
