# 🔑 VERDE V3.0 — HARDWARE HANDOFF SHEET (FOR AARAV)
### Everything the ESP32 code needs to talk to the cloud. Write your own code — just use EXACTLY these values and formats.

---

## 1️⃣ FIREBASE REALTIME DATABASE (both boards use this)

| Item | Value |
|---|---|
| **FIREBASE_HOST** | `verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app` |
| **FIREBASE_AUTH (legacy DB secret)** | `v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl` |
| Console (see data live) | https://console.firebase.google.com/project/verde-tech-haha/database/verde-tech-haha-default-rtdb/data |

⚠️ HOST = bare hostname. **NO `https://`, NO trailing `/`.**

**Arduino library:** `Firebase ESP32 Client` by **Mobizt** (Library Manager).
Connect with:
```cpp
fbConfig.host = FIREBASE_HOST;
fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
Firebase.begin(&fbConfig, &fbAuth);
```

**REST alternative (works from anything, even curl):**
```
GET  https://verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app/controls.json?auth=v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl
PUT  https://verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app/sensors/moisture.json?auth=v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl   (body: 52)
```

---

## 2️⃣ DATABASE SCHEMA — WRITE/READ EXACTLY THESE PATHS

### 📤 Main Brain WRITES → `/sensors` (every 4 seconds)
| Path | Type | Meaning |
|---|---|---|
| `/sensors/moisture` | int 0–100 | soil moisture % |
| `/sensors/temperature` | float | °C |
| `/sensors/humidity` | float | % |
| `/sensors/lux` | int | light level |
| `/sensors/tank_level` | int 0–100 | bucket water % |
| `/sensors/last_updated` | timestamp | **REQUIRED! Dashboard shows OFFLINE if this stops updating for 10s.** Use `Firebase.setTimestamp(fbData, "/sensors/last_updated")` |

### 📥 Main Brain READS → `/controls` (every loop)
| Path | Type | Meaning |
|---|---|---|
| `/controls/manual_mode` | bool | true = obey app toggles, false = autonomous |
| `/controls/pump_state` | bool | in manual: turn pump ON/OFF. In auto: BOARD writes this back so app shows pump status |
| `/controls/grow_light_state` | bool | same pattern for UV LED |
| `/controls/moisture_threshold` | int 0–100 | auto-water when moisture < this |
| `/controls/weather_override` | int 0/1 | 1 = rain predicted → DON'T water |
| `/controls/capture_photo` | bool | CAM watches this |

### 📤 Main Brain WRITES (optional, every 5 min) → history for the chart
`/historical_logs/moisture_log/{epoch_seconds}` = moisture int
(key = epoch seconds as string, e.g. `/historical_logs/moisture_log/1784264500`)

### 📸 ESP32-CAM logic
1. Poll `/controls/capture_photo` every 2s
2. If `true` → flash ON → capture JPEG → flash OFF
3. POST the raw JPEG to the upload API (section 3)
4. The SERVER resets the flag to false — but also reset it yourself if the POST fails

---

## 3️⃣ PHOTO UPLOAD API (ESP32-CAM only)

| Item | Value |
|---|---|
| **URL** | `https://VERCEL-DOMAIN/api/upload-photo` ← ⚠️ ASK ANUJ for the final domain after Vercel deploy (planned: `https://verde-ka-app.vercel.app/api/upload-photo`) |
| **Method** | POST |
| **Header 1** | `Content-Type: image/jpeg` |
| **Header 2** | `x-api-key: 119a08a6c901ef59e49fcbe77e4bf1c105467a9c69f17a0f` |
| **Body** | raw JPEG bytes (`http.POST(fb->buf, fb->len)`) |
| **Max size** | 400 KB (SVGA + jpeg_quality 10 ≈ 60KB — perfect) |

**Responses:**
- `200 {"success":true,...}` → done, server already reset the flag
- `401` → x-api-key wrong/missing
- `415` → body wasn't a JPEG
- `507` → image too big, lower quality/resolution

⚠️ **NEVER localhost. NEVER an IP. Only the https Vercel domain.**

**Camera settings that are PROVEN to work (from our own testing):**
```cpp
config.xclk_freq_hz = 8000000;      // 8MHz — kills Wi-Fi RF interference!
config.frame_size   = FRAMESIZE_SVGA; // 800x600
config.jpeg_quality = 10;
config.fb_count     = 1;
// + WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);  // disable brownout
// + esp_camera_fb_return(fb);  // ALWAYS free the buffer after POST
```

---

## 4️⃣ WHAT THE HARDWARE DOES *NOT* NEED (server handles these — don't put them in ESP32 code!)

| API | Who uses it | Key location |
|---|---|---|
| OpenWeatherMap | Vercel cron → writes `/controls/weather_override` | server env only |
| crop.health (Kindwise) | Vercel → leaf diagnosis | server env only |
| Gemini | Vercel → treatment text | server env only |

The board just reads `weather_override` from Firebase. Zero weather code needed on the ESP32. 🎯

---

## 5️⃣ QUICK SELF-TEST COMMANDS (run in any terminal/browser)

```bash
# See all live data:
curl "https://verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app/.json?auth=v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl"

# Fake a moisture write (dashboard gauge should move instantly!):
curl -X PUT "https://verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app/sensors/moisture.json?auth=v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl" -d "77"

# Trigger the camera manually:
curl -X PUT "https://verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app/controls/capture_photo.json?auth=v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl" -d "true"
```

---

## 6️⃣ PIN MAP (agreed wiring — dashboard labels assume this)
DHT22 DATA→**GPIO4** · HC-SR04 TRIG→**18** ECHO→**19** · Soil AO→**34**, gated VCC→**23** (HIGH 15–20ms only during read!) · LDR→**35** · Pump relay IN1→**25** (ACTIVE-LOW) · UV LED→**26** (active-high, 220Ω)

**Reference implementations** (working code to steal from): `Code_1_Main_Brain.ino` & `Code_2_ESP32_CAM.ino` in this same folder.
