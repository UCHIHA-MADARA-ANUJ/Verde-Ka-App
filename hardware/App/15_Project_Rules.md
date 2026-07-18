# 15. Strict Project Rules

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
