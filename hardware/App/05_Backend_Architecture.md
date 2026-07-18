# 05. Next.js Backend & Serverless API Routes

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
  * If `"rain"`, `"drizzle"`, or `"thunderstorm"` is found, writes `weather_override = 1` in Firebase under `/Garden/WeatherOverride`.
  * If clear, writes `weather_override = 0`.
