// ============================================================
// PROJECT VERDE V3.0 — RTDB PATH CONSTANTS (single source of truth)
// Mirrors the schema in App/07_Database_Design.md
// ============================================================
export const PATHS = {
  SENSORS: "/sensors",
  CONTROLS: "/controls",
  MOISTURE_LOG: "/historical_logs/moisture_log",
  LATEST_SCAN: "/latest_scan",
};

export const SENSOR_DEFAULTS = {
  moisture: 0,
  temperature: 0,
  humidity: 0,
  lux: 0,
  tank_level: 0,
  last_updated: 0,
};

export const CONTROL_DEFAULTS = {
  manual_mode: false,
  pump_state: false,
  grow_light_state: false,
  moisture_threshold: 40,
  weather_override: 0,
  capture_photo: false,
};

// Device is considered OFFLINE if last_updated is older than this (ms)
export const OFFLINE_TIMEOUT_MS = 10000;
