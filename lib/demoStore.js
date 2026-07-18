"use client";
// ============================================================
// VERDE DEMO STORE — full ESP32 simulation engine.
// Activates automatically when Firebase env vars are missing,
// so the dashboard is 100% demoable with zero setup — and doubles
// as the exhibition fallback if venue Wi-Fi dies mid-demo.
//
// Simulates: soil moisture decay + pump irrigation physics,
// reservoir drain, day/night lux cycle, DHT22 wobble, autonomous
// botanist logic (threshold / dry-run lockout / weather override),
// and on-demand camera capture with a bundled leaf photo.
// ============================================================

const TICK_MS = 2000;

let state = {
  sensors: {
    moisture: 52,
    temperature: 24.5,
    humidity: 65.0,
    lux: 800,
    tank_level: 85,
    last_updated: Date.now(),
  },
  controls: {
    manual_mode: false,
    pump_state: false,
    grow_light_state: false,
    moisture_threshold: 40,
    weather_override: 0,
    capture_photo: false,
  },
  weather: {
    condition: "Clear",
    description: "clear sky",
    temp: 31,
    city: "Delhi",
    synced_at: Date.now(),
  },
  latest_scan: null,
};

const listeners = new Set();
let timer = null;
let t = 0; // tick counter for cycles

function emit() {
  const snapshot = {
    sensors: { ...state.sensors },
    controls: { ...state.controls },
    weather: { ...state.weather },
    latest_scan: state.latest_scan ? { ...state.latest_scan } : null,
  };
  listeners.forEach((fn) => fn(snapshot));
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function tick() {
  t++;
  const s = state.sensors;
  const c = state.controls;

  // --- Day/night lux cycle (~3 min period) + noise ---
  const phase = Math.sin((t * TICK_MS) / 90000 * Math.PI * 2);
  s.lux = clamp(Math.round(650 + phase * 550 + (Math.random() * 60 - 30)), 100, 1200);

  // --- DHT22 ambient wobble ---
  s.temperature = clamp(
    +(s.temperature + (Math.random() * 0.4 - 0.2)).toFixed(1), 18, 38
  );
  s.humidity = clamp(
    +(s.humidity + (Math.random() * 1.2 - 0.6)).toFixed(1), 30, 95
  );

  // --- Autonomous botanist logic (mirrors Code_1_Main_Brain.ino) ---
  if (!c.manual_mode) {
    c.pump_state =
      s.moisture < c.moisture_threshold &&
      s.tank_level > 10 &&
      c.weather_override === 0;
    c.grow_light_state = s.lux < 400;
  } else if (s.tank_level <= 10) {
    c.pump_state = false; // dry-run protection overrides even manual mode
  }

  // --- Irrigation physics ---
  if (c.pump_state) {
    s.moisture = clamp(+(s.moisture + 2.2).toFixed(0), 0, 100);
    s.tank_level = clamp(+(s.tank_level - 0.6).toFixed(0), 0, 100);
  } else {
    s.moisture = clamp(+(s.moisture - 0.18).toFixed(2), 0, 100);
  }

  s.last_updated = Date.now();
  emit();
}

function ensureRunning() {
  if (!timer && typeof window !== "undefined") {
    timer = setInterval(tick, TICK_MS);
  }
}

// ---------------- Public API (mirrors the Firebase hooks) ----------------

export function demoSubscribe(fn) {
  listeners.add(fn);
  fn({
    sensors: { ...state.sensors },
    controls: { ...state.controls },
    weather: { ...state.weather },
    latest_scan: state.latest_scan ? { ...state.latest_scan } : null,
  });
  ensureRunning();
  return () => listeners.delete(fn);
}

export function demoSetControl(patch) {
  state.controls = { ...state.controls, ...patch };
  emit();
}

/** Simulated ESP32-CAM: flag flips true, "captures" for 2.5s, then
 *  resets the flag and drops a bundled leaf scan into latest_scan. */
export function demoRequestCapture() {
  state.controls = { ...state.controls, capture_photo: true };
  emit();
  setTimeout(() => {
    state.controls = { ...state.controls, capture_photo: false };
    state.latest_scan = {
      imageUrl: "/demo_leaf.jpg",
      captured_at: Date.now(),
      status: "uploaded",
      demo: true,
    };
    emit();
  }, 2500);
  return Promise.resolve();
}

/** Canned Verde AI diagnosis for demo scans (no API keys needed). */
export const DEMO_DIAGNOSIS = {
  plant_identified: "Ocimum tenuiflorum (Tulsi / Holy Basil)",
  health_diagnosis: "Early Leaf Spot traces (82% confidence)",
  gemini_remedy:
    "1. Mix 5ml neem oil + 2ml mild soap in 1L water; spray both leaf faces at dusk, twice weekly.\n" +
    "2. Remove the 2-3 worst spotted leaves to stop spore spread.\n" +
    "3. Lower moisture target to 40% — damp foliage feeds the fungus.\n" +
    "4. Ensure the UV grow light runs during cloudy hours (lux < 400) for stronger leaf tissue.\n" +
    "5. Re-scan foliage in 3 days. If spots spread, repeat neem cycle for 2 weeks.\n" +
    "Prognosis: excellent — early-stage and fully recoverable.",
};
