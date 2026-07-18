# 18. Development Implementation Checklist

Use this checklist to track your development progress step-by-step.

---

## 🏁 Phase 1: Firebase Project Setup
* [ ] Create a new project on the Firebase Console.
* [ ] Initialize a **Realtime Database** (RTDB) in test mode.
* [ ] Enable **Firebase Cloud Storage** (default bucket).
* [ ] Enable **Anonymous Authentication** in the Auth tab.
* [ ] Add your API keys and RTDB URL to your Next.js `.env.local` file.

## 🏁 Phase 2: Next.js Web Client Setup
* [ ] Initialize Next.js project using `npx create-next-app@latest`.
* [ ] Install core dependencies: `firebase`, `recharts`, `framer-motion`, `lucide-react`.
* [ ] Create your `lib/firebase.js` initialization script.
* [ ] Set up background Anonymous authentication on dashboard load.

## 🏁 Phase 3: Telemetry Gauges & Chart
* [ ] Create the radial moisture ring gauge.
* [ ] Create the filling blue water reservoir cylinder (from `tank_level`).
* [ ] Add the Temperature, Humidity, and Lux card widgets.
* [ ] Implement the Recharts `AreaChart` plotting live moisture logs.

## 🏁 Phase 4: Overrides & Firebase Cloud Sync
* [ ] Bind your Manual/Auto toggle switch to change `manual_mode` in Firebase RTDB.
* [ ] Bind your target threshold slider to change `moisture_threshold` in Firebase.
* [ ] Set up the serverless OpenWeatherMap weather check endpoint.

## 🏁 Phase 5: Camera & AI Integrations
* [ ] Code the Next.js `/api/upload-photo` endpoint to handle binary image streams.
* [ ] Bind your "Scan Foliage" dashboard button to write `capture_photo = true` in Firebase.
* [ ] Code the `/api/analyze-plant` route (connecting Plant.id and Gemini 2.0 Flash APIs).
* [ ] Embed the captured photo and Gemini response into the dashboard's AI chatbot console.
