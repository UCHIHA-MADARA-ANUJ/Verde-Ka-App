# 🌱 Verde Tech V3.0 — Autonomous Plant OS (Web Client)

The complete **Track B** implementation for Project Verde V3.0: a cyberpunk
Next.js control deck with Firebase RTDB real-time sync, AI plant diagnostics
(Plant.id + Gemini 2.0 Flash), Delhi weather-aware irrigation and a 15-day
storage TTL — built exactly to the specs in `main-app-details/verde-main/App/`.

---

## 🗂️ What's inside

```
verde-app/
├── app/
│   ├── page.js                     # Terminal boot splash → /dashboard
│   ├── dashboard/page.js           # Single-page control deck (12-col grid)
│   └── api/
│       ├── upload-photo/route.js   # ESP32-CAM JPEG buffer → Firebase Storage (Node)
│       ├── analyze-plant/route.js  # Plant.id → Gemini 2.0 Flash remedy chain (Edge)
│       ├── weather-sync/route.js   # Hourly Delhi OpenWeatherMap cron → weather_override
│       └── cleanup-storage/route.js# Nightly 15-day TTL scan deletion cron
├── components/                     # Gauges, cylinder, chart, control deck, AI terminal, toasts
├── lib/
│   ├── firebase.js                 # Lazy web client + Anonymous Auth session
│   ├── firebaseAdmin.js            # Admin SDK (server routes only)
│   ├── paths.js                    # RTDB schema constants
│   └── hooks/                      # useTelemetry / useControls / useMoistureHistory / useLatestScan
├── firebase/
│   ├── database.rules.json         # auth != null locked RTDB rules
│   └── storage.rules               # public-read /scans, auth-write
└── vercel.json                     # Cron schedules (hourly weather, nightly cleanup)
```

## ◈ DEMO MODE (zero-setup preview + exhibition fallback)

**No Firebase keys? No problem.** If the `NEXT_PUBLIC_FIREBASE_*` env vars are
absent, the dashboard automatically boots into **DEMO MODE** — a full local
ESP32 simulation (`lib/demoStore.js`):

- Soil moisture decays over time; the **autonomous botanist** fires the pump
  when it drops below the target (respecting the dry-run lockout & weather override)
- Pump runs raise moisture and drain the reservoir — watch the cylinder drop
- Day/night lux cycle triggers the UV grow light below 400 lux
- Manual mode, all toggles and the threshold slider work exactly like production
- **Scan Plant Foliage** simulates the ESP32-CAM (flag flips, 2.5s capture,
  bundled Tulsi leaf photo) and prints a canned Verde AI diagnosis — no API keys needed
- A purple "DEMO MODE · SIMULATED EDGE" badge makes the state obvious

This doubles as the **DAV ACON 5 contingency plan**: if venue Wi-Fi dies,
present the dashboard in demo mode while the physical build runs autonomously.

```bash
npm install && npm run dev   # → http://localhost:3000/dashboard (demo mode)
```

---

## ⚡ Feature checklist (vs App/18_Development_Checklist.md)

- ✅ Anonymous Auth boot (no login screen for judges)
- ✅ Radial glowing moisture gauge + target threshold marker
- ✅ Blue reservoir cylinder — flashing red CRITICAL card below 10% (dry-run lockout)
- ✅ Temp / Humidity / Lux cards (Lux card turns purple when UV grow light is on)
- ✅ Recharts glowing AreaChart — 24h window from `/historical_logs/moisture_log` + live points
- ✅ Manual/Auto toggle, moisture target slider, pump & UV LED actuator toggles (sub-100ms writes)
- ✅ "EDGE OFFLINE" red pulsing badge + frozen controls when `last_updated` >10s stale
- ✅ Weather badge + "Rain predicted — irrigation suspended" banner
- ✅ Scan Plant Foliage → `capture_photo=true` → spinner released when flag resets
- ✅ Foliage viewport with scanline animation + monospace Gemini chatbot terminal
- ✅ Toasts: grow light activation, irrigation complete (+5% moisture)
- ✅ `x-api-key` guard on uploads, JPEG magic-byte validation, 2MB cap
- ✅ 15-day TTL cleanup cron · hourly Delhi weather cron (`vercel.json`)
- ✅ Zero hardcoded secrets — everything via env vars

---

## 🚀 Setup & Deploy

### 1. Firebase Console
1. Create a project → enable **Realtime Database**, **Cloud Storage**, and
   **Anonymous Authentication**.
2. Paste `firebase/database.rules.json` into RTDB → Rules.
3. Paste `firebase/storage.rules` into Storage → Rules.
4. Project Settings → add a **Web app** → copy the client config.
5. Project Settings → Service accounts → **Generate new private key** (for the
   Admin SDK env vars).

### 2. Environment variables
```bash
cp .env.example .env.local   # fill in every value
```
On Vercel, add the same variables under **Project → Settings → Environment
Variables**. Never commit `.env.local`.

### 3. Run locally
```bash
npm install
npm run dev        # http://localhost:3000
```

### 4. Deploy to Vercel
```bash
npx vercel --prod
```
`vercel.json` auto-registers both crons. Set `CRON_SECRET` so the cron routes
reject outside callers.

### 5. Point the hardware at production
- `Code_2_ESP32_CAM.ino` → set `UPLOAD_URL` to
  `https://<your-app>.vercel.app/api/upload-photo` and `UPLOAD_API_KEY` to the
  same value as `CAM_UPLOAD_API_KEY`. **Never localhost!**
- `Code_1_Main_Brain.ino` → fill Wi-Fi + Firebase host/secret.

---

## 🔌 RTDB Schema (single source of truth: `lib/paths.js`)

```json
{
  "sensors":  { "moisture": 52, "temperature": 24.5, "humidity": 65.0,
                "lux": 800, "tank_level": 85, "last_updated": 1784264500000 },
  "controls": { "manual_mode": false, "pump_state": false,
                "grow_light_state": false, "moisture_threshold": 40,
                "weather_override": 0, "capture_photo": false },
  "historical_logs": { "moisture_log": { "<epoch>": 52 } },
  "latest_scan": { "imageUrl": "...", "captured_at": 0, "status": "uploaded" },
  "weather": { "condition": "Clear", "temp": 31, "city": "Delhi", "synced_at": 0 }
}
```

Built by Aarav & Anuj · DAV ACON 5 · Ready to win 🏆
