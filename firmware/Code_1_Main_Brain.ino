// =========================================================================
// PROJECT VERDE V3.0 — CODE 1: MAIN CONTROL DECK (ESP32 WROOM DEV KIT)
// Target Board: "DOIT ESP32 DEVKIT V1" (or "ESP32 Dev Module")
// Sourcing: Sits on the Techtonics 30-Pin Breakout Shield
// =========================================================================

#include <WiFi.h>
#include <DHT.h>
#include <FirebaseESP32.h> // Ensure "Firebase ESP32 Client" by Mobizt is installed!

// -------------------------------------------------------------------------
// 🌐 NETWORK & CLOUD CONFIGURATION
// -------------------------------------------------------------------------
#define WIFI_SSID "YOUR_WIFI_HOTSPOT_NAME"       // Enter your phone hotspot name
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"   // Enter your hotspot password
#define FIREBASE_HOST "YOUR_PROJECT_ID.firebaseio.com" // Enter your Firebase RTDB URL (without http:// or https://)
#define FIREBASE_AUTH "YOUR_DATABASE_SECRET"   // Enter your Firebase Database Secret Key

// -------------------------------------------------------------------------
// 🔌 G-V-S HARDWARE PIN MAPPING
// -------------------------------------------------------------------------
#define DHTPIN 4               // DHT22/DHT11 Data connected to G-V-S Port 4
#define DHTTYPE DHT22          // Change to DHT11 if using a blue DHT11 sensor
#define TRIG_PIN 18            // HC-SR04 Trigger connected to G-V-S Port 18
#define ECHO_PIN 19            // HC-SR04 Echo connected to G-V-S Port 19
#define SOIL_PIN 34            // 2-Prong Soil Moisture Analog connected to G-V-S Port 34
#define LDR_PIN 35             // LDR Light Analog connected to G-V-S Port 35
#define MOISTURE_POWER_PIN 23  // 2-Prong VCC Power connected to G-V-S Port 23 (For Power Gating!)
#define PUMP_RELAY 25          // Robocraze Relay IN1 connected to G-V-S Port 25
#define UV_LED_PIN 26          // Everlight 5mm UV LED Positive connected to G-V-S Port 26

// -------------------------------------------------------------------------
// 🧠 GLOBAL INSTANCES & VARIABLES
// -------------------------------------------------------------------------
DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbData;
FirebaseConfig fbConfig;
FirebaseAuth fbAuth;

unsigned long lastUploadTime = 0; // Throttle timer for database publishing
const unsigned long uploadInterval = 4000; // Publish data to Firebase every 4 seconds

// Sensor Telemetry Variables
int moisturePct = 0;
float temperature = 0.0;
float humidity = 0.0;
int tankPct = 0;
int luxLevel = 0;

// -------------------------------------------------------------------------
// 🛠️ INITIALIZATION & CONFIGURATION (BOOT DECK)
// -------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== PROJECT VERDE V3.0: MAIN CONTROL DECK INITIALIZING ===");
  
  dht.begin();
  
  // Pin Mode Configurations
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(PUMP_RELAY, OUTPUT);
  pinMode(UV_LED_PIN, OUTPUT);
  pinMode(MOISTURE_POWER_PIN, OUTPUT);
  
  // Safe Default Actuator States (Active Low Relay, Active High LED)
  digitalWrite(PUMP_RELAY, HIGH);        // Relay HIGH = Pump OFF
  digitalWrite(UV_LED_PIN, LOW);         // GPIO LOW = UV LED OFF
  digitalWrite(MOISTURE_POWER_PIN, LOW);   // GPIO LOW = Moisture Probe unpowered (Corrosion prevention!)

  // Connect to Wi-Fi Hotspot
  Serial.print("Connecting to Wi-Fi Hotspot: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected successfully!");
  Serial.print("Local IP Address: ");
  Serial.println(WiFi.localIP());

  // Firebase Configuration
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);
  
  Serial.println("Firebase Realtime Database handshake complete.");
  Serial.println("=========================================================");
}

// -------------------------------------------------------------------------
// 🔄 CORE SYSTEM LOOP (SENSORS & AUTONOMOUS/MANUAL COORDINATION)
// -------------------------------------------------------------------------
void loop() {
  // --- 1. READ SENSORS ---
  
  // Power-Gated 2-Prong Soil Moisture Reading (Stops Electrolysis & Rust!)
  digitalWrite(MOISTURE_POWER_PIN, HIGH);  // Turn sensor Power ON
  delay(20);                               // Wait 20ms for analog voltage to stabilize
  int rawMoisture = analogRead(SOIL_PIN);  // Read raw voltage
  digitalWrite(MOISTURE_POWER_PIN, LOW);   // Turn sensor Power OFF immediately!
  
  // Map raw 12-bit Analog voltage (0-4095) to percentage (0% to 100%)
  // Calibrate these numbers: Wet reading in water (~1200), Dry reading in air (~4095)
  moisturePct = map(rawMoisture, 4095, 1200, 0, 100); 
  moisturePct = constrain(moisturePct, 0, 100);

  // Read DHT22 Temperature & Humidity
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  if (isnan(temperature)) temperature = 24.5; // Fail-safe fallback values
  if (isnan(humidity)) humidity = 60.0;

  // Read Water Level in Bucket via HC-SR04 Ultrasonic Distance Sensor
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

  // Read Ambient Light level via LDR Sensor
  int ldrRaw = analogRead(LDR_PIN);
  luxLevel = map(ldrRaw, 0, 4095, 100, 1200); // Approximate lux conversion

  // --- 2. CLOUD TELEMETRY PUBLISH (4-SECOND THROTTLE) ---
  if (millis() - lastUploadTime > uploadInterval) {
    lastUploadTime = millis();
    
    Firebase.setInt(fbData, "/sensors/moisture", moisturePct);
    Firebase.setFloat(fbData, "/sensors/temperature", temperature);
    Firebase.setFloat(fbData, "/sensors/humidity", humidity);
    Firebase.setInt(fbData, "/sensors/tank_level", tankPct);
    Firebase.setInt(fbData, "/sensors/lux", luxLevel);
    // Heartbeat timestamp — the dashboard marks the edge OFFLINE if this
    // stops updating for >10 seconds (App/12_Offline_and_Error_Handling.md)
    Firebase.setTimestamp(fbData, "/sensors/last_updated");
    
    Serial.printf("TELEMETRY -> Moisture: %d%% | Temp: %.1fC | Tank: %d%% | Light: %d LUX\n", 
                  moisturePct, temperature, tankPct, luxLevel);
  }

  // --- 2B. HISTORICAL MOISTURE LOG (5-MINUTE THROTTLE) ---
  // Feeds the dashboard's 24h Recharts AreaChart without spamming the DB.
  static unsigned long lastLogTime = 0;
  if (millis() - lastLogTime > 300000UL) { // every 5 minutes
    lastLogTime = millis();
    // Read the server heartbeat (ms epoch). Use doubleData() — a ms epoch
    // (~1.75e12) overflows a 32-bit int, so never use intData() here!
    if (Firebase.getDouble(fbData, "/sensors/last_updated")) {
      unsigned long long epochSec = (unsigned long long)(fbData.doubleData() / 1000.0);
      String logPath = "/historical_logs/moisture_log/" + String((unsigned long)epochSec);
      Firebase.setInt(fbData, logPath.c_str(), moisturePct);
    }
  }

  // --- 3. DYNAMIC CONTROL COORDINATION (MANUAL OVERRIDES vs AUTONOMY) ---
  bool manualMode = false;
  int threshold = 40;
  int weatherOverride = 0;

  // Read real-time user-defined flags from Firebase RTDB
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
    // --- MODE A: MANUAL APP OVERRIDES ---
    bool forcePump = false, forceLights = false;
    Firebase.getBool(fbData, "/controls/pump_state");
    forcePump = fbData.boolData();
    Firebase.getBool(fbData, "/controls/grow_light_state");
    forceLights = fbData.boolData();

    // Trigger relays/pins immediately
    digitalWrite(PUMP_RELAY, forcePump ? LOW : HIGH);   // Active-Low relay
    digitalWrite(UV_LED_PIN, forceLights ? HIGH : LOW); // Active-High GPIO
  } 
  else {
    // --- MODE B: AUTONOMOUS SMART BOTANIST ---
    
    // Pump logic: Turn ON only if Soil is Dry AND Bucket has water (>10%) AND No forecast rain
    if (moisturePct < threshold && tankPct > 10 && weatherOverride == 0) {
      digitalWrite(PUMP_RELAY, LOW); // Turn pump ON
      Firebase.setBool(fbData, "/controls/pump_state", true);
    } else {
      digitalWrite(PUMP_RELAY, HIGH); // Turn pump OFF
      Firebase.setBool(fbData, "/controls/pump_state", false);
    }

    // Grow Light logic: Turn ON only if ambient light falls below 400 LUX (cloudy/dark hour)
    if (luxLevel < 400) {
      digitalWrite(UV_LED_PIN, HIGH); // Turn UV LED ON
      Firebase.setBool(fbData, "/controls/grow_light_state", true);
    } else {
      digitalWrite(UV_LED_PIN, LOW);  // Turn UV LED OFF
      Firebase.setBool(fbData, "/controls/grow_light_state", false);
    }
  }
}
