# 08. API Endpoint Specifications

This document outlines the REST API routes running on Vercel to support the Next.js frontend and ESP32-CAM nodes.

---

## 🔌 1. API Endpoint Reference

### A. Image Upload Route
* **Endpoint:** `POST /api/upload-photo`
* **Runtime:** Node.js (Buffer handling)
* **Headers:**
  * `Content-Type: image/jpeg`
  * `x-api-key: your-secure-cam-key` (Prevents unauthorized image uploads)
* **Request Body:** Raw binary JPEG image buffer.
* **Success Response (200 OK):**
```json
{
  "success": true,
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/verde-project.appspot.com/o/scans%2Fcurrent.jpg"
}
```
* **Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Invalid API Key header"
}
```

### B. Plant Leaf AI Diagnosis
* **Endpoint:** `POST /api/analyze-plant`
* **Runtime:** Edge Runtime
* **Headers:**
  * `Content-Type: application/json`
* **Request Body:**
```json
{
  "imageUrl": "https://firebasestorage.googleapis.com/v0/b/verde-project.appspot.com/o/scans%2Fcurrent.jpg"
}
```
* **Success Response (200 OK):**
```json
{
  "plant_identified": "Ocimum tenuiflorum (Tulsi)",
  "health_diagnosis": "Leaf Spot Disease (89% confidence)",
  "gemini_remedy": "Fungus spots detected. Spray organic neem-oil water mixture weekly, and reduce moisture threshold to 40%."
}
```

### C. Weather Forecast Sync
* **Endpoint:** `GET /api/weather-sync`
* **Runtime:** Edge Runtime
* **Description:** Hourly cron schedule. Fetches forecast for Delhi from OpenWeatherMap and writes `weather_override` to Firebase.
* **Success Response (200 OK):**
```json
{
  "success": true,
  "weather": "Rain",
  "override_written": 1
}
```
