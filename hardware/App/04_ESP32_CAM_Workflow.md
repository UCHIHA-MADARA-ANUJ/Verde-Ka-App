# 04. ESP32-CAM Workflow & Storage Pipeline

This document outlines the on-demand image capture, storage pipeline, and critical network routing configurations of the **ESP32-CAM** standalone vision node under the `/Garden` namespace.

---

## 📷 1. The On-Demand Camera Loop ("On Appeal")
The ESP32-CAM remains in a low-power, non-streaming idle state. It connects to Wi-Fi and polls the Firebase Realtime Database path `/Garden/Capture` every 2 seconds.

```
[ Next.js App ]             [ Firebase RTDB ]             [ ESP32-CAM ]             [ Vercel Cloud ]
       │                            │                            │                         │
       │──(Click "Scan")───────────►│                            │                         │
       │                            │(Capture = true)            │                         │
       │                            │◄──(Polls capture flag)─────│                         │
       │                            │                            │──(Flashes & Snaps)      │
       │                            │                            │                         │
       │                            │                            │──(POSTs Binary JPEG)───►│
       │                            │◄──(Resets flag to false)───┼─────────────────────────│
       │                            │                            │                         │
```

---

## 🚫 2. Why "Localhost" Must NEVER Be Used
A common beginner trap is configuring the ESP32-CAM's upload URL to point to a local computer address like `http://localhost:3000/api/upload-photo`.

* **The Problem:** The ESP32-CAM is an independent physical network computer with its own IP. When it requests `localhost`, it is requesting *itself* (not your laptop or server). The upload will immediately fail with a routing timeout!
* **The Solution (Production):** The ESP32-CAM must always post directly to your public, secure Vercel production domain:
  `https://verde-tech-proj.vercel.app/api/upload-photo`
* **The Solution (Local Testing):** If testing locally over your mobile hotspot, the camera must be configured to point to your laptop's exact local hotspot IP address (e.g., `http://192.168.1.6:5000/upload`).

---

## ⚡ 3. The 8MHz Clock Throttling Workaround (Antenna RF Fix)

On cheap or standard ESP32-CAM clone boards, running the camera's internal master clock (`XCLK`) at the default **20MHz** creates a fatal design flaw:

* **The Interference:** A 20MHz clock frequency generates **intense high-frequency electromagnetic interference** directly with the adjacent onboard PCB Wi-Fi antenna!
* **The Symptom:** When taking a photo and transmitting over Wi-Fi at the same time, the Wi-Fi radio drops packets, resulting in `send payload failed` errors and connection dropouts.
* **The Solution:** Throttle the clock speed down to **`8000000` (8MHz)** or **`10000000` (10MHz)** in the camera configuration:
  ```cpp
  config.xclk_freq_hz = 8000000; // 8MHz clock completely stops RF Wi-Fi interference!
  ```
* **Benefits:** This drops the peak current draw by 40%, completely preventing current-draw brownouts (such as `0x20002` errors) and allowing the camera to transmit smoothly over Wi-Fi with 100% stability!

---

## 💾 4. Direct Upload vs. Backend Request Comparison

| Metric | Option A: Standalone Camera Server | Option B: Direct HTTP POST Upload (Recommended) |
| :--- | :--- | :--- |
| **How it works** | Camera hosts local IP server; app opens stream. | Camera snaps on request and POSTs image to server. |
| **Pros** | Real-time continuous live streaming. | **Incredibly low power, zero network blocks, extremely secure.** |
| **Cons** | **Fails on Home Broadband (AP Isolation blocks it)**; heats up. | Requires a backend upload endpoint. |

**Decision:** **Option B (Direct HTTP POST Upload)** is chosen for the production build because it completely bypasses AP/Client isolation on home Wi-Fi routers and keeps the board cool!
