// =========================================================================
// PROJECT VERDE V3.0 — MAIN BRAIN CONTROL DECK FIRMWARE
// Target Microcontroller: DOIT ESP32 DevKit V1 (30-Pin, CP2102, Type-C)
// Sourcing: Sits on your desk, wired directly via half-size breadboard
// Author: Aarav Choudhary (Class 10th Student & Championship IoT Engineer)
// =========================================================================

#include <WiFi.h>
#include <FirebaseESP32.h> // Ensure "Firebase ESP32 Client" by Mobizt is installed!
#include <DHT.h>

// -------------------------------------------------------------------------
// 🌐 NETWORK & CLOUD INTERFACE CONFIGURATION
// -------------------------------------------------------------------------
#define WIFI_SSID "CCA SCHOOL"               // Hotspot SSID
#define WIFI_PASSWORD "admin@123"            // Hotspot Password
#define FIREBASE_HOST "verde-tech-haha-default-rtdb.asia-southeast1.firebasedatabase.app" // Handed over from Anuj!
#define FIREBASE_AUTH "v7IcV45UuyozAhKaWyHBl4DvmNVoKjzBf1sh2tyl"                         // Handed over from Anuj!

// -------------------------------------------------------------------------
// 🔌 G-V-S HARDWARE PIN MAPPING (METICULOUSLY ALIGNED WITH PATHS AND PINS)
// -------------------------------------------------------------------------
#define DHTPIN 4               // DHT22/DHT11 Data Line connected to GPIO 4
#define DHTTYPE DHT11          // Change to DHT22 if using a white DHT22 sensor
#define TRIG_PIN 18            // HC-SR04 Ultrasonic Trigger Pin connected to GPIO 18
#define ECHO_PIN 19            // HC-SR04 Ultrasonic Echo Pin connected to GPIO 19
#define SOIL_PIN 34            // 2-Prong Moisture Sensor Analog AO connected to GPIO 34 (ADC1_CH6 - Isolated from Wi-Fi)
#define MOISTURE_POWER_PIN 23  // 2-Prong Gated VCC connected to GPIO 23 (For active power-gating)
#define LDR_PIN 35             // 4-Pin LDR Sensor Analog INV connected to GPIO 35 (ADC1_CH7 - Isolated from Wi-Fi)
#define PUMP_RELAY 25          // Robocraze 5V Relay IN1 connected to GPIO 25 (Active-Low)
#define UV_LED_PIN 26          // Everlight 5mm UV LED connected to GPIO 26 (Active-High via 220-Ohm Resistor)

// -------------------------------------------------------------------------
// 🧠 GLOBAL INSTANCES, CALIBRATION CONSTANTS & STATE VARIABLES
// -------------------------------------------------------------------------
DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

// Non-Blocking Millis Timing Registers
unsigned long lastUploadTime = 0; 
const unsigned long uploadInterval = 1000; // Continuous 1-second telemetry stream to match previous app performance!

unsigned long lastWiFiCheck = 0;
const unsigned long wifiRetryInterval = 5000; // Background Wi-Fi health check every 5 seconds

// Sensor Telemetry Buffers
int soilPerc = 0;
float currentTemp = 0.0;
float currentHum = 0.0;
int tankPct = 0;
int luxLevel = 0;

// System Controls State Registers (Fully synced bidirectionally over WebSockets)
bool manualMode = false;         // false = Auto (Smart Botanist), true = Manual (App Overrides)
bool isPumpRunning = false;      // Track pump state to prevent duplicate switching
bool ledState = false;           // Track LED state to prevent duplicate switching
int moistureThreshold = 30;     // Moisture threshold below which the pump auto-triggers (Default: 30%)
int weatherOverride = 0;         // 1 = Rain predicted in Delhi (irrigation suspended), 0 = Normal
bool lastCaptureFlag = false;    // Monitor capture_photo trigger line

// -------------------------------------------------------------------------
// 🛠️ SYSTEM SETUP & Wi-Fi DEEP HANDSHAKE
// -------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(30);
  Serial.println("\n=========================================================");
  Serial.println("=== PROJECT VERDE V3.0: MAIN CONTROL DECK INITIALIZING ===");
  Serial.println("=========================================================");
  
  dht.begin();
  
  // Pin Mode Configurations
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(PUMP_RELAY, OUTPUT);
  pinMode(UV_LED_PIN, OUTPUT);
  pinMode(MOISTURE_POWER_PIN, OUTPUT);
  pinMode(SOIL_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  
  // Hard Safe States (Relays are active-low, UV LED is active-high)
  digitalWrite(PUMP_RELAY, HIGH);        // Relay HIGH = Pump OFF
  digitalWrite(UV_LED_PIN, LOW);         // GPIO LOW = UV LED OFF
  digitalWrite(MOISTURE_POWER_PIN, LOW);   // Soil sensor gated OFF by default

  // Establish Wi-Fi Connection
  Serial.printf("[WIFI] Connecting to network: %s \n", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int connectTries = 0;
  while (WiFi.status() != WL_CONNECTED && connectTries < 30) {
    delay(250);
    Serial.print(".");
    connectTries++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected Successfully!");
    Serial.print("[WIFI] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI] WiFi connection failed. Entering local autonomous fallback mode.");
  }

  // Initialize Firebase Connection
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
  
  // Set default startup values under /controls to initialize the database
  if (WiFi.status() == WL_CONNECTED) {
    Firebase.setBool(fbData, "/controls/manual_mode", false);
    Firebase.setBool(fbData, "/controls/pump_state", false);
    Firebase.setBool(fbData, "/controls/grow_light_state", false);
    Firebase.setInt(fbData, "/controls/moisture_threshold", 30);
    Firebase.setInt(fbData, "/controls/weather_override", 0);
    Firebase.setBool(fbData, "/controls/capture_photo", false);
    Serial.println("[FB] Cloud handshake complete. Default variables initialized.");
  }

  // Visual Setup Signal (Single Blink)
  digitalWrite(UV_LED_PIN, HIGH); delay(120); digitalWrite(UV_LED_PIN, LOW); delay(120);
  Serial.println("[SYSTEM] Setup completed. Verde OS V3.0 active.");
  Serial.println("=========================================================");
}

// -------------------------------------------------------------------------
// 🔄 CORE SYSTEM LOOP (SENSORS & AUTONOMOUS/MANUAL COORDINATION)
// -------------------------------------------------------------------------
void loop() {
  unsigned long now = millis();

  // --- 1. NON-BLOCKING BACKING WI-FI HEALTH MONITOR ---
  if (WiFi.status() != WL_CONNECTED && (now - lastWiFiCheck >= wifiRetryInterval)) {
    lastWiFiCheck = now;
    Serial.println("[WIFI] Connection lost! Attempting background reconnect...");
    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  }

  // --- 2. SENSOR DECK (READING ENVIRONMENT & TELEMETRY) ---
  
  // A. Power-Gated Soil Moisture Reading (Stops prong rust!)
  digitalWrite(MOISTURE_POWER_PIN, HIGH);  // Turn sensor power ON
  delay(15);                               // Wait 15ms for analog voltage to stabilize
  int rawMoisture = analogRead(SOIL_PIN);  // Read raw 12-bit analog voltage
  digitalWrite(MOISTURE_POWER_PIN, LOW);   // Turn sensor power OFF immediately!
  
  // Map 12-bit ESP32 analog range (0-4095) to percentage (0% to 100%)
  // Calibrate these numbers based on soil: Dry in air (~4095), Wet in water (~1200)
  soilPerc = map(rawMoisture, 4095, 1200, 0, 100); 
  soilPerc = constrain(soilPerc, 0, 100);

  // B. High-Precision Analog LDR Light Reading (Bypasses WiFi ADC2 conflict!)
  int rawLdr = analogRead(LDR_PIN);
  // Map 12-bit input (0-4095) to raw light percentage
  int lightPct = map(rawLdr, 4095, 1200, 0, 100);
  lightPct = constrain(lightPct, 0, 100);
  luxLevel = lightPct * 10;                // Approximate Lux scaling
  isDark = (lightPct < 35);                // Hysteresis: It is dark if light level is under 35%

  // C. DHT22 Ambient Temperature & Humidity Reads
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (!isnan(h) && !isnan(t)) {
    currentHum = h;
    currentTemp = t;
  }

  // D. Water Level Cylinder Reading (HC-SR04)
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  // Convert distance to remaining bucket percentage (Assumes 20cm deep bucket)
  // 18cm distance to surface is empty (0%), 2cm distance to surface is full (100%)
  tankPct = map(distance, 18, 2, 0, 100);
  tankPct = constrain(tankPct, 0, 100);

  // --- 3. CLOUD TELEMETRY PUSH & WEB CLIENT SYNC (1-SECOND STREAM) ---
  if (WiFi.status() == WL_CONNECTED && (now - lastUploadTime >= uploadInterval)) {
    lastUploadTime = now;
    
    // Write telemetry strictly under the /sensors path as per Anuj's handoff!
    Firebase.setInt(fbData, "/sensors/moisture", soilPerc);
    Firebase.setFloat(fbData, "/sensors/temperature", currentTemp);
    Firebase.setFloat(fbData, "/sensors/humidity", currentHum);
    Firebase.setInt(fbData, "/sensors/lux", luxLevel);
    Firebase.setInt(fbData, "/sensors/tank_level", tankPct);
    
    // Required Timestamp Heartbeat: If this stops updating, dashboard marks device as OFFLINE
    Firebase.setTimestamp(fbData, "/sensors/last_updated");

    // Pull current user adjustments from Firebase RTDB over WebSockets
    if (Firebase.getBool(fbData, "/controls/manual_mode")) {
      manualMode = fbData.boolData();
    }
    if (Firebase.getInt(fbData, "/controls/moisture_threshold")) {
      moistureThreshold = fbData.intData();
    }
    if (Firebase.getInt(fbData, "/controls/weather_override")) {
      weatherOverride = fbData.intData();
    }

    Serial.printf("[TELEMETRY] Moisture:%d%% | Temp:%.1fC | Hum:%.1f%% | Tank:%d%% | Light:%d Lux | Mode:%s\n", 
                  soilPerc, currentTemp, currentHum, tankPct, luxLevel, manualMode ? "MANUAL" : "AUTO");
  }

  // --- 4. DECISION ENGINE (MANUAL OVERRIDES vs AUTONOMOUS SMART OS) ---
  bool requestPumpOn = false;
  bool requestLedOn = false;

  if (manualMode) {
    // --- MODE A: MANUAL APP OVERRIDES ---
    // Read forced trigger flags written by user on Next.js buttons
    if (WiFi.status() == WL_CONNECTED) {
      bool forcePump = false, forceLights = false;
      Firebase.getBool(fbData, "/controls/pump_state");
      forcePump = fbData.boolData();
      Firebase.getBool(fbData, "/controls/grow_light_state");
      forceLights = fbData.boolData();

      requestPumpOn = forcePump;
      requestLedOn = forceLights;
    }
  } 
  else {
    // --- MODE B: AUTONOMOUS PRECISION BOTANIST ---
    
    // Pump auto-triggers only if: Soil Moisture is low AND Reservoir has water (>10%) AND No rain override active
    if (soilPerc < moistureThreshold && tankPct > 10 && weatherOverride == 0) {
      requestPumpOn = true;
    } else {
      requestPumpOn = false;
    }

    // Grow Light auto-triggers based on LDR Dark sensor state
    requestLedOn = isDark;
  }

  // --- 5. PHYSICAL ACTUATOR DRIVE DECK ---
  
  // Water Pump Relay Drive (Active Low)
  if (requestPumpOn && !isPumpRunning) {
    digitalWrite(PUMP_RELAY, LOW); // Turn pump ON
    isPumpRunning = true;
    Serial.println("[PUMP] START");
    if (!manualMode && WiFi.status() == WL_CONNECTED) {
      Firebase.setBool(fbData, "/controls/pump_state", true); // Sync state back to app
    }
  } 
  else if (!requestPumpOn && isPumpRunning) {
    digitalWrite(PUMP_RELAY, HIGH); // Turn pump OFF
    isPumpRunning = false;
    Serial.println("[PUMP] STOP");
    if (!manualMode && WiFi.status() == WL_CONNECTED) {
      Firebase.setBool(fbData, "/controls/pump_state", false); // Sync state back to app
    }
  }

  // Everlight 5mm UV LED Drive (Active High)
  if (requestLedOn && !ledState) {
    digitalWrite(UV_LED_PIN, HIGH); // Turn UV LED ON
    ledState = true;
    Serial.println("[LED] GLOW");
    if (!manualMode && WiFi.status() == WL_CONNECTED) {
      Firebase.setBool(fbData, "/controls/grow_light_state", true); // Sync state back to app
    }
  } 
  else if (!requestLedOn && ledState) {
    digitalWrite(UV_LED_PIN, LOW);  // Turn UV LED OFF
    ledState = false;
    Serial.println("[LED] SHUT");
    if (!manualMode && WiFi.status() == WL_CONNECTED) {
      Firebase.setBool(fbData, "/controls/grow_light_state", false); // Sync state back to app
    }
  }

  delay(40); // 40ms wait for loop responsiveness
}
