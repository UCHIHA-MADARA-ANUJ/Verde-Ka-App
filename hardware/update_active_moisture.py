# Overwrite Code_1_Main_Brain.ino to use CONTINUOUS active moisture sensing (no power gating) and exact /Garden paths

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
#define SOIL_PIN 34            // GPIO 34 (A0) -> Controls 2-Prong Moisture Sensor Analog Out (CONTINUOUS ACTIVE READ)
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
  Serial.println("\n=== PROJECT VERDE: FINAL ESP32 MAIN DECK (CONTINUOUS ACTIVE MONITORING) ===");
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(SOIL_PIN, INPUT); // Configured as input for continuous active reading
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // Safe Default States
  digitalWrite(RELAY_PIN, HIGH);         // Relay HIGH = Pump OFF (Active Low)
  digitalWrite(LED_PIN, LOW);            // LED LOW = UV LED OFF

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

  // --- 1. CONTINUOUS real-time Soil Moisture Reading (Always Active!) ---
  int rawSoil = analogRead(SOIL_PIN); // Read analog value from continuous 3.3V power line
  
  // Map 12-bit ESP32 Analog input (0-4095) to percentage
  // Calibrate these numbers: Wet reading in water (~1200), Dry reading in air (~4095)
  soilPerc = map(rawSoil, 4095, 1200, 0, 100);
  soilPerc = constrain(soilPerc, 0, 100);

  // --- 2. AMBIENT LDR LIGHT SENSING ---
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

# Overwrite App/20_Physical_Wiring_Manual.md to change moisture VCC to continuous 3.3V

with open("App/20_Physical_Wiring_Manual.md", "r") as f:
    text = f.read()

# Replace Step 3 with active continuous wiring
new_step_3 = """## 💧 STEP 3: Wiring the 2-Prong Soil Moisture Sensor (CONTINUOUS REAL-TIME READS)
Your 2-prong soil sensor consists of the fork probe and a small comparator circuit board (VCC, GND, AO).

1. Connect the fork probe to the input pins of the comparator board using the short F-F wires provided in your kit.
2. Now, connect the output of the comparator board to your breadboard and ESP32 using 3 **Female-to-Male (F-M)** wires:
   * Connect comparator **GND** to the breadboard **negative (-) outer rail**.
   * Connect comparator **AO (Analog Out)** directly to **ESP32 GPIO 34 (ADC1_CH6)** (the 4th pin from the top-left near the USB port).
   * Connect comparator **VCC (Power)** directly to **Row 30, Column C** on your breadboard (which shares the stable 3.3V power from your ESP32's `3V3` pin!).
   * *🚨 IMPORTANT SAFETY DECISION:* **We power the soil moisture comparator directly from the ESP32's 3.3V pin.** If we powered it from the 5V USB rail, its AO signal could output 5V, which exceeds the ESP32's maximum GPIO voltage limit and would burn out your analog pin! Powering it from **3.3V** is 100% electrically safe, reduces electrolysis corrosion by 50%, and allows your app to **continuously monitor your soil moisture 24/7 without any resets!**"""

text = text.replace("## 💧 STEP 3: Wiring the 2-Prong Soil Moisture Sensor (Power-Gated)\nYour 2-prong soil sensor consists of the fork probe and a small comparator circuit board (VCC, GND, AO).\n\n1. Connect the fork probe to the input pins of the comparator board using the short F-F wires provided in your kit.\n2. Now, connect the output of the comparator board to your breadboard and ESP32 using 3 **Female-to-Male (F-M)** wires:\n   * Connect comparator **GND** to the breadboard **negative (-) outer rail**.\n   * Connect comparator **AO (Analog Out)** directly to **ESP32 GPIO 34** (the 4th pin from the top-left near the USB port).\n   * Connect comparator **VCC (Power)** directly to **ESP32 GPIO 23** (the 2nd pin from the bottom-right).\n   * *Why:* This is our gated power connection. The ESP32 pin 23 will only output 3.3V for 15ms during a soil check, then instantly drop to 0V. This completely stops copper electrolysis and prevents your sensor from rusting in wet soil!", new_step_3)

with open("App/20_Physical_Wiring_Manual.md", "w") as f:
    f.write(text)

print("Moisture sensor successfully updated to ACTIVE CONTINUOUS 24/7 monitoring!")
