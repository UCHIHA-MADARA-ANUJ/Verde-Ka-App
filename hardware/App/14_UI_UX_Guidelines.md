# 14. UI/UX Guidelines & Themes

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
