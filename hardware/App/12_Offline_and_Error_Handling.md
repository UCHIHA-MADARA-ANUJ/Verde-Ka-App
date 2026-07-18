# 12. Offline and Error Handling

This document outlines the hard-fault, network drop, and device-offline recovery strategies designed into the system.

---

## 🚨 1. Hard-Fault Recovery Scenarios

### A. ESP32 Main Brain Offline
* **Trigger:** Next.js dashboard detects that the sensor `last_updated` timestamp in Firebase RTDB is older than 10 seconds.
* **App Display:** The dashboard displays a red pulsing badge: *"⚠️ EDGE OFFLINE: System operating autonomously"*. It freezes the manual control switches to prevent user command congestion.
* **Local Recovery:** The ESP32 continues running its local, independent loops. If soil moisture falls below target, it still waters locally, ensuring your plant survives even if Wi-Fi dies!

### B. ESP32-CAM Capture Failure (Brownout/Voltage Sag)
* **Trigger:** Next.js API times out waiting for the binary POST upload from the camera.
* **App Display:** The app sets `/Garden/Capture = false` in Firebase, stops the user loading spinner, and slides in an error toast: *"❌ Scan Failed: Insufficient power on camera node. Retrying..."*
* **Local Recovery:** ESP32-CAM clears its frame buffer RAM instantly using `esp_camera_fb_return(fb)` to prevent memory leaks and crashes, returning to its idle state.

---

## 🛠️ 2. Network State Recovery Matrix

| Fault State | Consequence | App UI Behavior | Physical Device Behavior |
| :--- | :--- | :--- | :--- |
| **Hotspot Offline** | No data reaches Firebase. | Displays "Device Offline" with last cached values. | ESP32 runs autonomous watering locally; retries WiFi every 5s. |
| **Database Down** | Controls cannot be synced. | Displays "Cloud Sync Error" banner. | ESP32 falls back to local threshold controls. |
| **User Closes App** | Manual actions stop. | N/A (Session preserved). | ESP32 instantly reverts to autonomous smart watering. |
