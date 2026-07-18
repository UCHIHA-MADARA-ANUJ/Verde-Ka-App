# Overwrite Code_1_Main_Brain.ino with the exact matching /Garden paths and pins

with open("Code_1_Main_Brain.ino", "w") as f:
    f.write("""// =========================================================================
// PROJECT VERDE V3.0 — CODE 1: MAIN CONTROL DECK (ESP32 WROOM DEV KIT)
// Target Board: "DOIT ESP32 DEVKIT V1" (or "ESP32 Dev Module")
// Sourcing: Sits on your desk, wired directly via half-size breadboard
// =========================================================================

#include <WiFi.h>
#include <FirebaseESP32.h> // Ensure "Firebase ESP32 Client" by Mobizt is installed!
#include <DHT.h>

// -------------------------------------------------------------------------
// 🌐 NETWORK & CLOUD CONFIGURATION
// -------------------------------------------------------------------------
#define WIFI_SSID "CCA SCHOOL"               // Enter your school/home hotspot name
#define WIFI_PASSWORD "admin@123"            // Enter your hotspot password
#define FIREBASE_HOST "verde-tech-b8ed3-default-rtdb.firebaseio.com" // Your exact database URL
#define FIREBASE_AUTH "AIzaSyA0duozMyYPxqKfDmmPyi23vxc5xB3D6wU"     // Your exact database secret

// -------------------------------------------------------------------------
// 🔌 BREADBOARD PIN MAPPING (MATCHES YOUR PHYSICAL SETUP)
// -------------------------------------------------------------------------
#define RELAY_PIN 5            // GPIO 5 (D1) -> Controls Water Pump Relay (Active Low)
#define DHT_PIN 4              // GPIO 4 (D2) -> Controls DHT Ambient Sensor
#define LDR_PIN 14             // GPIO 14 (D5) -> Controls LDR Light Sensor Digital Comparator
#define LED_PIN 12             // GPIO 12 (D6) -> Controls Everlight 5mm UV LED (Active High)
#define SOIL_PIN 34            // GPIO 34 (A0) -> Controls 2-Prong Moisture Sensor Analog Out
#define MOISTURE_POWER_PIN 23  // GPIO 23 -> Gated VCC pin for soil sensor (Corrosion prevention!)
#define TRIG_PIN 18            // GPIO 18 -> HC-SR04 Ultrasonic Trigger
#define ECHO_PIN 19            // GPIO 19 -> HC-SR04 Ultrasonic Echo

// -------------------------------------------------------------------------
// 🧠 GLOBAL INSTANCES & VARIABLES
// -------------------------------------------------------------------------
#define DHTTYPE DHT11          // Change to DHT22 if using a DHT22 white sensor
DHT dht(DHT_PIN, DHTTYPE);

FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

unsigned long lastUploadTime = 0; 
const unsigned long uploadInterval = 1000; // Fast telemetry stream (1 second) to match previous code!

// Telemetry & State Variables
int soilPerc = 0;
float currentTemp = 0.0;
float currentHum = 0.0;
bool isPumpRunning = false;
bool ledState = false;
bool isDark = false;
int threshold = 30;
String mode = "MANUAL";

// -------------------------------------------------------------------------
// 🛠️ INITIALIZATION & Wi-Fi DECK
// -------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(30);
  Serial.println("\n=== PROJECT VERDE: FINAL ESP32 MAIN DECK (PRO-LEVEL ASSEMBLY) ===");
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(MOISTURE_POWER_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // Safe Default States
  digitalWrite(RELAY_PIN, HIGH);         // Relay HIGH = Pump OFF (Active Low)
  digitalWrite(LED_PIN, LOW);            // LED LOW = UV LED OFF
  digitalWrite(MOISTURE_POWER_PIN, LOW);   // Sensor power gated OFF initially

  dht.begin();
  delay(1000);

  // Connect to Wi-Fi
  Serial.printf("[WIFI] Connecting to %s ", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 40) {
    delay(200);
    Serial.print(".");
    tries++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected successfully! IP:");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI] Offline mode active.");
  }

  // Firebase Configuration
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
  
  // Set default startup values in Cloud
  if (WiFi.status() == WL_CONNECTED) {
    Firebase.setString(fbData, "/Garden/Pump", "OFF");
    Firebase.setString(fbData, "/Garden/LED", "OFF");
    Firebase.setString(fbData, "/Garden/Mode", "MANUAL");
  }
  
  // Boot blink signal
  digitalWrite(LED_PIN, HIGH); delay(120); digitalWrite(LED_PIN, LOW); delay(120);
  Serial.println("[SYSTEM] Ready.");
}

// -------------------------------------------------------------------------
// 🔄 MAIN LOOP: DYNAMIC CONTROLS & AUTO/MANUAL STATE COORDINATION
// -------------------------------------------------------------------------
void loop() {
  unsigned long now = millis();

  // --- 1. POWER-GATED MOISTURE SENSING (ANTI-RUST) ---
  digitalWrite(MOISTURE_POWER_PIN, HIGH); // Turn sensor VCC ON
  delay(15);                              // Wait for voltage to settle
  int rawSoil = analogRead(SOIL_PIN);
  digitalWrite(MOISTURE_POWER_PIN, LOW);  // Turn sensor VCC OFF immediately!
  
  // Map 12-bit ESP32 Analog input (0-4095) to percentage
  soilPerc = map(rawSoil, 4095, 1200, 0, 100);
  soilPerc = constrain(soilPerc, 0, 100);

  // --- 2. AMBIENT LDR LIGHT SENSING ---
  // Reads digital comparator output: HIGH means Dark (depending on your module potentiometer calibration)
  isDark = (digitalRead(LDR_PIN) == HIGH);

  // --- 3. SAFE TEMPERATURE & HUMIDITY READING ---
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (!isnan(h) && !isnan(t)) {
    currentHum = h;
    currentTemp = t;
  }

  // --- 4. ULTRASONIC WATER LEVEL SENSING (HC-SR04) ---
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  // Convert distance to bucket percentage (Assumes 20cm deep bucket)
  int tankLevelPct = map(distance, 18, 2, 0, 100);
  tankLevelPct = constrain(tankLevelPct, 0, 100);

  // --- 5. FAST TELEMETRY PUSH & CLOUD SYNC (1-SECOND INTERVAL) ---
  if (WiFi.status() == WL_CONNECTED && (now - lastUploadTime >= uploadInterval)) {
    lastUploadTime = now;
    
    // Publish sensor updates under your exact /Garden paths!
    Firebase.setInt(fbData, "/Garden/Moisture", soilPerc);
    Firebase.setFloat(fbData, "/Garden/Temperature", currentTemp);
    Firebase.setInt(fbData, "/Garden/Humidity", (int)currentHum);
    Firebase.setString(fbData, "/Garden/Light", isDark ? "Dark" : "Bright");
    Firebase.setInt(fbData, "/Garden/TankLevel", tankLevelPct);
    
    // Sync mode and threshold variables in real-time from app
    if (Firebase.getString(fbData, "/Garden/Mode")) {
      String cloudMode = fbData.stringData();
      if (cloudMode != "" && cloudMode != mode) {
        mode = cloudMode;
        Serial.printf("[SYNC] Mode from cloud: %s\n", mode.c_str());
      }
    }
    if (Firebase.getInt(fbData, "/Garden/Threshold")) {
      threshold = fbData.intData();
    }

    // Dynamic Reservoir Warnings: Trigger in-app warnings & prevent pump dry-runs
    int tankThreshold = 20;
    if (Firebase.getInt(fbData, "/Garden/TankThreshold")) {
      tankThreshold = fbData.intData();
    }
    if (tankLevelPct < tankThreshold) {
      Firebase.setBool(fbData, "/Garden/TankWarning", true);
    } else {
      Firebase.setBool(fbData, "/Garden/TankWarning", false);
    }

    Serial.printf("[STATUS] Soil:%d%% | Temp:%.1fC | Hum:%d%% | Tank:%d%% | Mode:%s | isDark:%s\n",
                  soilPerc, currentTemp, (int)currentHum, tankLevelPct, mode.c_str(), isDark ? "DARK" : "BRIGHT");
  }

  // --- 6. COORDINATE CONTROL DECISIONS (AUTO / MANUAL) ---
  bool requestPumpOn = false;
  bool requestLedOn = false;

  // Sync manual control variables from Firebase
  String cloudPump = "OFF";
  String cloudLed = "OFF";
  int weatherOverride = 0;

  if (WiFi.status() == WL_CONNECTED) {
    if (Firebase.getString(fbData, "/Garden/Pump")) cloudPump = fbData.stringData();
    if (Firebase.getString(fbData, "/Garden/LED"))  cloudLed = fbData.stringData();
    if (Firebase.getInt(fbData, "/Garden/WeatherOverride")) weatherOverride = fbData.intData();
  }

  if (mode == "MANUAL") {
    // --- MODE A: STRICT MANUAL CONTROL ---
    requestPumpOn = (cloudPump == "ON" || cloudPump == "1");
    requestLedOn = (cloudLed == "ON" || cloudLed == "1");
  } 
  else {
    // --- MODE B: AUTONOMOUS SMART CONTROL ---
    // Pump auto triggers if soil moisture drops below threshold AND bucket is not empty (>10%) AND no rain override is active
    if (soilPerc < threshold && tankLevelPct > 10 && weatherOverride == 0) {
      requestPumpOn = true;
    } else {
      requestPumpOn = false;
    }

    // Grow Light auto triggers based on LDR Dark detection
    requestLedOn = isDark;
  }

  // --- 7. HARDWARE ACTUATION DECK ---
  
  // Water Pump Relay (Active Low)
  if (requestPumpOn && !isPumpRunning) {
    digitalWrite(RELAY_PIN, LOW); // Turn pump ON
    isPumpRunning = true;
    Serial.println("[PUMP] START");
    if (mode == "AUTO" && WiFi.status() == WL_CONNECTED) {
      Firebase.setString(fbData, "/Garden/Pump", "ON");
    }
  } 
  else if (!requestPumpOn && isPumpRunning) {
    digitalWrite(RELAY_PIN, HIGH); // Turn pump OFF
    isPumpRunning = false;
    Serial.println("[PUMP] STOP");
    if (mode == "AUTO" && WiFi.status() == WL_CONNECTED) {
      Firebase.setString(fbData, "/Garden/Pump", "OFF");
    }
  }

  // Everlight 5mm UV LED (Active High)
  if (requestLedOn && !ledState) {
    digitalWrite(LED_PIN, HIGH); // Turn LED ON
    ledState = true;
    Serial.println("[LED] GLOW");
    if (mode == "AUTO" && WiFi.status() == WL_CONNECTED) {
      Firebase.setString(fbData, "/Garden/LED", "ON");
    }
  } 
  else if (!requestLedOn && ledState) {
    digitalWrite(LED_PIN, LOW);  // Turn LED OFF
    ledState = false;
    Serial.println("[LED] SHUT");
    if (mode == "AUTO" && WiFi.status() == WL_CONNECTED) {
      Firebase.setString(fbData, "/Garden/LED", "OFF");
    }
  }

  delay(40); // 40ms wait for loop responsiveness
}
""")

# Overwrite Code_2_ESP32_CAM.ino with the exact matching /Garden paths

with open("Code_2_ESP32_CAM.ino", "w") as f:
    f.write("""// =========================================================================
// PROJECT VERDE V3.0 — CODE 2: STANDALONE AI CAMERA (ESP32-CAM)
// Target Board: "AI Thinker ESP32-CAM"
// Sourcing: Powered independently, mounted on the MB USB Programmer Shield
// =========================================================================

#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include <FirebaseESP32.h> // Ensure "Firebase ESP32 Client" by Mobizt is installed!
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

// -------------------------------------------------------------------------
// 🌐 NETWORK & CLOUD CONFIGURATION
// -------------------------------------------------------------------------
#define WIFI_SSID "CCA SCHOOL"               // Enter your school/home hotspot name
#define WIFI_PASSWORD "admin@123"            // Enter your hotspot password
#define FIREBASE_HOST "verde-tech-b8ed3-default-rtdb.firebaseio.com" // Your exact database URL
#define FIREBASE_AUTH "AIzaSyA0duozMyYPxqKfDmmPyi23vxc5xB3D6wU"     // Your exact database secret

// Next.js API route that receives raw binary JPEG data
#define UPLOAD_URL "https://verde-tech-proj.vercel.app/api/upload-photo"

// -------------------------------------------------------------------------
// 🔌 AI-THINKER ESP32-CAM CAMERA PINOUT CONFIGURATION
// -------------------------------------------------------------------------
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

#define FLASH_LED_PIN 4  // Bright white on-board flash LED

// -------------------------------------------------------------------------
// 🧠 GLOBAL INSTANCES & VARIABLES
// -------------------------------------------------------------------------
FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

unsigned long lastTriggerCheck = 0;
const unsigned long checkInterval = 2000; // Poll Firebase every 2 seconds for scan requests

// -------------------------------------------------------------------------
// 🛠️ CAMERA INITIALIZATION FUNCTION
// -------------------------------------------------------------------------
bool initCamera() {
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
  
  // 🚨 THE CRITICAL HARDWARE WORKAROUND:
  // Throttling the XCLK clock speed from 20MHz down to 8MHz completely eliminates
  // high-frequency RF interference with the Wi-Fi PCB antenna and cuts peak current draw!
  config.xclk_freq_hz = 8000000; 
  
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_SVGA; // 800x600 high resolution (optimal for Plant Disease AI)
  config.jpeg_quality = 10;           // High JPEG quality (lower number = higher quality)
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera initialization failed with error: 0x%x\n", err);
    return false;
  }
  Serial.println("Camera successfully initialized!");
  return true;
}

// -------------------------------------------------------------------------
// 🛠️ INITIALIZATION & Wi-Fi DECK
// -------------------------------------------------------------------------
void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout resets
  Serial.begin(115200);
  Serial.println("\n=== PROJECT VERDE V3.0: STANDALONE CAMERA NODE INITIALIZING ===");

  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW); // Flash OFF by default

  // 1. Initialize Camera FIRST (WiFi is OFF to prevent power surge!)
  if (!initCamera()) {
    Serial.println("Fatal: Camera Init Failed! Retrying...");
    delay(2000);
    ESP.restart(); // Hard reboot if camera is not detected
  }

  delay(500); // Wait for power to settle

  // 2. Connect to WiFi hotspot
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected successfully!");
  Serial.print("Local IP Address: ");
  Serial.println(WiFi.localIP());

  // 3. Initialize Firebase Connection
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
  
  Serial.println("Firebase RTDB sync active. Waiting for capture commands under /Garden/Capture...");
  Serial.println("=========================================================");
}

// -------------------------------------------------------------------------
// 🔄 CAMERA TRIGGER POLLING LOOP (LISTEN & EXECUTE "ON APPEAL")
// -------------------------------------------------------------------------
void loop() {
  if (millis() - lastTriggerCheck > checkInterval) {
    lastTriggerCheck = millis();

    bool captureRequested = false;
    
    // Poll Firebase Realtime Database for the trigger flag under /Garden/Capture
    if (Firebase.getBool(fbData, "/Garden/Capture")) {
      captureRequested = fbData.boolData();
    }

    if (captureRequested) {
      Serial.println("📸 Capture command detected in Firebase! Processing...");
      
      // 1. Turn the Flash LED ON
      digitalWrite(FLASH_LED_PIN, HIGH);
      delay(150); // Give the flash time to illuminate the plant leaf
      
      // 2. Capture the Frame
      camera_fb_t * fb = esp_camera_fb_get();
      
      // 3. Turn the Flash LED OFF immediately to prevent current spikes
      digitalWrite(FLASH_LED_PIN, LOW);

      if (!fb) {
        Serial.println("Error: Camera capture failed!");
        Firebase.setBool(fbData, "/Garden/Capture", false); // Clear flag in Firebase
        return;
      }

      Serial.println("Uploading photo wirelessly to Next.js App...");
      HTTPClient http;
      http.begin(UPLOAD_URL);
      http.addHeader("Content-Type", "image/jpeg");

      // Post raw binary image bytes directly over-the-air!
      int httpResponseCode = http.POST(fb->buf, fb->len);
      if (httpResponseCode > 0) {
        Serial.printf("Upload Successful! HTTP Response: %d\n", httpResponseCode);
        
        // Write the flag back to false in Firebase to tell the app the upload is complete!
        Firebase.setBool(fbData, "/Garden/Capture", false);
      } else {
        Serial.printf("Upload failed! Error: %s\n", http.errorToString(httpResponseCode).c_str());
        Firebase.setBool(fbData, "/Garden/Capture", false); // Clear flag anyway to reset state
      }
      
      http.end();
      esp_camera_fb_return(fb); // CRITICAL: Free RAM buffer immediately to prevent leaks!
      Serial.println("Capture complete! Returning to idle state.");
    }
  }
}
""")

print("Factual C++ Codes updated successfully on disk with your exact /Garden paths and pins!")
