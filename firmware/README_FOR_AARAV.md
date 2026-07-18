# 🔌 AARAV — FLASH GUIDE (2 minutes of edits, that's it)

Both `.ino` files already contain the REAL Firebase credentials.
You only need to change the lines marked `<<< AARAV`.

---

## CODE 1 — Main Brain (ESP32 DevKit V1)

Open `Code_1_Main_Brain.ino`, edit **only lines 14–15**:

```cpp
#define WIFI_SSID "AARAV_HOTSPOT_NAME"        // ← your phone hotspot name
#define WIFI_PASSWORD "AARAV_HOTSPOT_PASSWORD" // ← your hotspot password
```
Lines 16–17 (FIREBASE_HOST / FIREBASE_AUTH) are **already correct — DO NOT TOUCH.**

**Arduino IDE settings:**
- Board: `DOIT ESP32 DEVKIT V1`
- Port: COM7 (or whichever appears)
- Upload speed: 921600
- Libraries needed: `DHT sensor library` (Adafruit) + `Firebase ESP32 Client` by **Mobizt**

**Success looks like** (Serial Monitor @ 115200):
```
WiFi Connected successfully!
Firebase Realtime Database handshake complete.
TELEMETRY -> Moisture: 52% | Temp: 24.5C | Tank: 85% | Light: 800 LUX
```
→ At that moment the web dashboard gauges move LIVE. Anuj can confirm.

---

## CODE 2 — Camera (AI-Thinker ESP32-CAM)

Open `Code_2_ESP32_CAM.ino`, edit **only lines 17–18** (same hotspot creds).

⚠️ **Line 23 — UPLOAD_URL:** currently set to
`https://verde-ka-app.vercel.app/api/upload-photo`
**Ask Anuj for the real Vercel domain after he deploys** — if it's different,
change just the domain part. NEVER use localhost!

Line 25 (UPLOAD_API_KEY) is already correct — do not touch.

**Arduino IDE settings:**
- Board: `AI Thinker ESP32-CAM`
- Upload speed: 115200
- Remember the usual CAM flash procedure (IO0 jumper / MB shield button if needed)

**End-to-end test:** Anuj opens the dashboard → AI LAB → SCAN PLANT FOLIAGE →
your CAM's flash fires within ~5s → photo + AI diagnosis appear on screen. 🏆

---

## Calibration (after first boot, optional but recommended)

1. **Soil sensor** — watch Serial raw values: dry-in-air vs dipped-in-water.
   Adjust in Code 1: `map(rawMoisture, 4095, 1200, 0, 100)` → replace 4095
   with YOUR dry reading, 1200 with YOUR wet reading.
2. **Bucket depth** — Code 1 assumes 18cm = empty, 2cm = full:
   `map(distance, 18, 2, 0, 100)` → adjust to your bucket.

## Wiring reminder (already documented in the logbook)
DHT22→GPIO4 · HC-SR04 TRIG→18 ECHO→19 · Soil AO→34, gated VCC→23 ·
LDR→35 · Pump relay IN→25 (active-LOW) · UV LED→26 (via 220Ω)
