# Project Verde V3.0 — The Zero-Error Single-Brain Master Manual
### Complete, Unabridged Word-by-Word Execution Plan with ESP32 Expansion Shield

Aarav and Anuj, replacing the LED strip with a **5mm UV LED** is a fantastic engineering shortcut. 

Since a 5mm UV LED operates on low voltage (3.3V) and draws less than 20mA of current, **it can be driven directly from the ESP32's GPIO pin through a 220-Ohm resistor!** This eliminates the second relay entirely! 

You now only need a **Single-Channel 5V Relay Module** to control your water pump and replace your buggy old relay. This keeps your wiring incredibly clean, extremely cheap, and simple to assemble.

---

## 🗺️ 1. System Architecture (Single-Brain + Standalone Camera)

All sensors and the UV LED connect directly to your main ESP32 Brain via dedicated, plug-and-play **G-V-S ribbon connectors** on the expansion shield.

```
                       [ CLOUD PLATFORM: Firebase RTDB ]
                                      ▲
                                      │ (WiFi Connection)
                                      ▼
                        [ ESP32 DevKit V1 Main Brain ]
                                      ▲
                        [ 30-Pin Expansion Shield ]
                                      ▲
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
    [Plug-and-Play Port 34]   [Plug-and-Play Port 4 ]   [Plug-and-Play Port 25 ]
    - Capacitive Moisture     - DHT22 Temp/Humidity     - Single-Channel Relay
    - LDR Light (Port 35)     - HC-SR04 (Ports 18/19)     (Pump)
                              - 5mm UV LED (Port 26)
```

---

## 🛒 2. Master Sourcing & Purchase List

### A. Sourced from School or Home (FREE - Do NOT Buy!)
* [x] **5V Submersible Water Pump** (Reused from your previous project)
* [x] **DHT Temp & Humidity Sensor** (Reused from your previous project)
* [x] **LDR Light Sensor** (Reused from your previous project)
* [x] **1x 220-Ohm Resistor** (Sourced from school physics lab)
* [x] **1x 1000uF 16V Electrolytic Capacitor** (Sourced from school physics lab)
* [x] **1x 1N4007 Diode** (Sourced from school physics lab)
* [x] **Cardboard, Plastic Bucket, Cut Soda Bottle, and Tulsi Plant**

### B. Final School Purchase List (On Amazon.in)
*Search for these exact terms directly in the Amazon India search box:*

1. **"ESP32 DevKit V1 30-Pin Board"** (Qty: 1 | ~₹320)
2. **"ESP32-CAM with OV2640 Camera and MB Programmer Shield"** (Qty: 1 | ~₹650)
3. **"Single-Channel 5V Relay Module Optocoupler-Isolated"** (Qty: 1 | ~₹95) *(Replaces your buggy pump relay)*
4. **"5mm Round UV LED Pack"** (Qty: 1 | ~₹250) *(Replaces the grow light strip)*
5. **"HC-SR04 Ultrasonic Distance Sensor"** (Qty: 1 | ~₹80)
6. **"Capacitive Soil Moisture Sensor v1.2"** (Qty: 1 | ~₹70) *(Rust-proof soil sensor upgrade)*
7. **"MB102 Full-Size 830-Point Solderless Breadboard"** (Qty: 1 | ~₹150) *(Optional, but good for mounting)*
8. **"Assorted Jumper Wires Pack Male-to-Male and Female-to-Male"** (Qty: 1 | ~₹199)

* **TOTAL PROCUREMENT COST:** **~ ₹1,813** *(Extremely budget-friendly!)*

---

## ⚡ 3. Direct G-V-S Wire-by-Wire Connections (Word-by-Word)

To set up, simply snap your **ESP32 DevKit V1 board** directly into the female headers of your **Techtonics Expansion Shield**. Wire your sensors directly to the G-V-S pins of the shield:

| Sensor / Module | Sensor Pin | Connection on ESP32 Shield | Wire Type | Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **DHT Sensor** | VCC (+) | **G-V-S Port 4** -> V (VCC) pin | F-F | Power (5V) |
| | GND (-) | **G-V-S Port 4** -> G (GND) pin | F-F | Ground |
| | DATA (S) | **G-V-S Port 4** -> S (Signal) pin| F-F | Temperature & Humidity Data |
| **Capacitive Moisture**| VCC (+) | **G-V-S Port 34** -> V (VCC) pin | F-F | Power (5V) |
| | GND (-) | **G-V-S Port 34** -> G (GND) pin | F-F | Ground |
| | AOUT (S) | **G-V-S Port 34** -> S (Signal) pin| F-F | Soil Moisture Data |
| **LDR Light Sensor** | VCC (+) | **G-V-S Port 35** -> V (VCC) pin | F-F | Power (5V) |
| | GND (-) | **G-V-S Port 35** -> G (GND) pin | F-F | Ground |
| | AOUT (S) | **G-V-S Port 35** -> S (Signal) pin| F-F | Ambient Light Data |
| **HC-SR04** | VCC | **G-V-S Port 18** -> V (VCC) pin | F-F | Power (5V) |
| (Water Level) | GND | **G-V-S Port 18** -> G (GND) pin | F-F | Ground |
| | TRIGGER | **G-V-S Port 18** -> S (Signal) pin| F-F | Send Ultrasonic Pulse |
| | ECHO | **G-V-S Port 19** -> S (Signal) pin| F-F | Read Echo Pulse |
| **Single Relay (Pump)**| VCC (V) | **G-V-S Port 25** -> V (VCC) pin | F-M | Relay Power |
| | GND (G) | **G-V-S Port 25** -> G (GND) pin | F-M | Ground |
| | IN (S) | **G-V-S Port 25** -> S (Signal) pin| F-M | Pump Control Signal |

### Special Direct Actuator Connections (Relay-Free LED!):
* **The 5mm UV LED (Relay-Free Wiring):**
  1. Take your **5mm UV LED** (identify the longer leg as Positive, shorter leg as Negative).
  2. Solder or twist a **220-Ohm Resistor** in series to the Positive (+) leg.
  3. Connect the other end of the resistor to the **S (Signal) pin** of **G-V-S Port 26** of your expansion shield.
  4. Connect the shorter Negative (-) leg of the UV LED to the **G (GND) pin** of **G-V-S Port 26** of your expansion shield.
  5. *Now the ESP32 can safely turn on the UV LED using simple software digital commands!*

* **5V Submersible Water Pump Wiring:**
  1. Cut the positive (+) wire of your 5V Pump. Connect one side to the **Normally Open (NO)** contact of Relay 1.
  2. Connect the other side of the positive wire to the **Common (COM)** contact of Relay 1.
  3. Connect the negative (-) wire of the pump directly to any spare **G (GND)** pin on your expansion shield.
  4. Place your **1N4007 Diode** in parallel across your pump's terminals (silver stripe to positive wire, plain black side to negative wire) to block feedback.
  5. Connect any spare **V (VCC)** pin on your expansion shield to the **Common (COM)** contact of Relay 1.

---

## 💾 4. Complete Main Brain Code (Copy-Paste to ESP32)

Upload this unified code to your main ESP32 DevKit V1 Board. It reads all environmental sensors, connects to WiFi, and updates Firebase RTDB.

```cpp
#include <WiFi.h>
#include <DHT.h>
#include <FirebaseESP32.h>

#define WIFI_SSID "YOUR_WIFI_HOTSPOT_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define FIREBASE_HOST "YOUR_PROJECT.firebaseio.com"
#define FIREBASE_AUTH "YOUR_DATABASE_SECRET"

#define DHTPIN 4
#define DHTTYPE DHT22
#define TRIG_PIN 18
#define ECHO_PIN 19
#define SOIL_PIN 34
#define LDR_PIN 35
#define PUMP_RELAY 25
#define UV_LED_PIN 26

DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

unsigned long lastUploadTime = 0;

void setup() {
  Serial.begin(115200);                    // Local USB debugging
  
  dht.begin();
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(PUMP_RELAY, OUTPUT);
  pinMode(UV_LED_PIN, OUTPUT);
  
  digitalWrite(PUMP_RELAY, HIGH);  // Relays are active-low, HIGH is OFF
  digitalWrite(UV_LED_PIN, LOW);   // UV LED is active-high, LOW is OFF

  // WiFi Connection
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");

  // Firebase Configuration
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  // 1. Read Capacitive Soil Moisture
  int rawMoisture = analogRead(SOIL_PIN);
  int moisturePct = map(rawMoisture, 4095, 1200, 0, 100); // 12-bit Analog conversion
  moisturePct = constrain(moisturePct, 0, 100);

  // 2. Read Temperature and Humidity
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  if (isnan(temp)) temp = 24.5;
  if (isnan(hum)) hum = 60.0;

  // 3. Read Water level in Bucket via Ultrasonic Sensor
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  int tankPct = map(distance, 18, 2, 0, 100); // 18cm is Empty, 2cm is Full
  tankPct = constrain(tankPct, 0, 100);

  // 4. Read LDR Light level
  int ldrRaw = analogRead(LDR_PIN);
  int lux = map(ldrRaw, 0, 4095, 100, 1200);

  // 5. Upload Telemetry to Firebase RTDB (Every 4 seconds)
  if (millis() - lastUploadTime > 4000) {
    lastUploadTime = millis();
    Firebase.setInt(fbData, "/sensors/moisture", moisturePct);
    Firebase.setFloat(fbData, "/sensors/temperature", temp);
    Firebase.setFloat(fbData, "/sensors/humidity", hum);
    Firebase.setInt(fbData, "/sensors/tank_level", tankPct);
    Firebase.setInt(fbData, "/sensors/lux", lux);
    
    // Print diagnostic logs to the local serial monitor
    Serial.printf("Moisture: %d%% | Temp: %.1fC | Tank: %d%% | Light: %d LUX\n", moisturePct, temp, tankPct, lux);
  }

  // 6. Automated Control & Manual Sync Logic
  bool manualMode = false;
  int threshold = 40;
  int weatherOverride = 0;

  if (Firebase.getBool(fbData, "/controls/manual_mode")) {
    manualMode = fbData.boolData();
  }
  if (Firebase.getInt(fbData, "/controls/moisture_threshold")) {
    threshold = fbData.intData();
  }
  if (Firebase.getInt(fbData, "/controls/weather_override")) {
    weatherOverride = fbData.intData();
  }

  if (manualMode) {
    // Strictly manual app overrides
    bool forcePump = false, forceLights = false;
    Firebase.getBool(fbData, "/controls/pump_state");
    forcePump = fbData.boolData();
    Firebase.getBool(fbData, "/controls/grow_light_state");
    forceLights = fbData.boolData();

    digitalWrite(PUMP_RELAY, forcePump ? LOW : HIGH);
    digitalWrite(UV_LED_PIN, forceLights ? HIGH : LOW);
  } else {
    // Automated Smart Irrigation Logic
    if (moisturePct < threshold && tankPct > 10 && weatherOverride == 0) {
      digitalWrite(PUMP_RELAY, LOW); // Turn pump ON (Active Low Relay)
      Firebase.setBool(fbData, "/controls/pump_state", true);
    } else {
      digitalWrite(PUMP_RELAY, HIGH); // Turn pump OFF
      Firebase.setBool(fbData, "/controls/pump_state", false);
    }

    // Automated Grow Light Logic
    if (lux < 400) {
      digitalWrite(UV_LED_PIN, HIGH); // Turn UV LED ON (Active High GPIO)
      Firebase.setBool(fbData, "/controls/grow_light_state", true);
    } else {
      digitalWrite(UV_LED_PIN, LOW);  // Turn UV LED OFF
      Firebase.setBool(fbData, "/controls/grow_light_state", false);
    }
  }
}
```

---

## 💾 5. Standalone On-Demand ESP32-CAM Code

Upload this code to your ESP32-CAM. The camera remains in an idle low-power loop. It captures and uploads a photo only when the user sets `/controls/capture_photo` to `true` in the app.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include <FirebaseESP32.h>

#define WIFI_SSID "YOUR_WIFI_HOTSPOT_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define FIREBASE_HOST "YOUR_PROJECT.firebaseio.com"
#define FIREBASE_AUTH "YOUR_DATABASE_SECRET"

FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

// ESP32-CAM Pinout Configuration (AI-Thinker)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
  Serial.begin(115200);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA; // High Resolution JPEG
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x", err);
    return;
  }

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");

  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  bool captureRequested = false;
  if (Firebase.getBool(fbData, "/controls/capture_photo")) {
    captureRequested = fbData.boolData();
  }

  if (captureRequested) {
    Serial.println("Capture requested! Taking photo...");
    camera_fb_t * fb = esp_camera_fb_get();
    if(!fb) {
      Serial.println("Camera capture failed!");
      return;
    }

    // Connect and POST photo to Next.js upload endpoint
    HTTPClient http;
    http.begin("https://verde-tech-proj.vercel.app/api/upload-photo");
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.POST(fb->buf, fb->len);
    if (httpResponseCode > 0) {
      Serial.printf("Uploaded! Response: %d\n", httpResponseCode);
      // Set trigger flag back to false in Firebase to signify completion
      Firebase.setBool(fbData, "/controls/capture_photo", false);
    } else {
      Serial.printf("Upload failed: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    
    http.end();
    esp_camera_fb_return(fb); // Free buffer memory
  }
  delay(2000); // Check for commands every 2 seconds
}
```
