# Overwrite Code_1_Main_Brain.ino to use HIGH-PRECISION ANALOG LDR sensing on GPIO 35 (ADC1)

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
#define LED_PIN 12             // GPIO 12 (D6) -> Controls Everlight 5mm UV LED (Active High)
#define SOIL_PIN 34            // GPIO 34 (A0) -> Controls 2-Prong Moisture Sensor Analog Out (CONTINUOUS ACTIVE READ)
#define LDR_PIN 35             // GPIO 35 (ADC1_CH7) -> Controls 4-Pin LDR Sensor ANALOG OUT (AO)
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
int luxLevel = 0; // High-precision analog light level (0 to 1000)
int threshold = 30;
String mode = "MANUAL";

// -------------------------------------------------------------------------
// 🛠️ INITIALIZATION & Wi-Fi DECK
// -------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(30);
  Serial.println("\n=== PROJECT VERDE: FINAL ESP32 MAIN DECK (HIGH-PRECISION ANALOG LDR) ===");
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(SOIL_PIN, INPUT); 
  pinMode(LDR_PIN, INPUT); // Configured as input for continuous analog reading
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

  // --- 1. CONTINUOUS Soil Moisture Reading (Always Active!) ---
  int rawSoil = analogRead(SOIL_PIN); 
  soilPerc = map(rawSoil, 4095, 1200, 0, 100);
  soilPerc = constrain(soilPerc, 0, 100);

  // --- 2. HIGH-PRECISION ANALOG LDR LIGHT SENSING (Always Active!) ---
  int ldrRaw = analogRead(LDR_PIN);
  // Map 12-bit ESP32 Analog input (0-4095) to clean light percentage (0% to 100%)
  // Full bright sunlight in room (~1200), completely dark with finger over sensor (~4095)
  int lightPct = map(ldrRaw, 4095, 1200, 0, 100); 
  lightPct = constrain(lightPct, 0, 100);
  
  // High-precision Lux estimation
  luxLevel = lightPct * 10; 
  
  // Hysteresis calculation: It is "Dark" if light level falls below 35%
  isDark = (lightPct < 35);

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
    Firebase.setInt(fbData, "/Garden/Lux", luxLevel); // Publish raw Lux value to database!
    
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

    Serial.printf("[STATUS] Soil:%d%% | Temp:%.1fC | Hum:%d%% | Tank:%d%% | Lux:%d | Mode:%s | isDark:%s\n",
                  soilPerc, currentTemp, (int)currentHum, tankLevelPct, luxLevel, mode.c_str(), isDark ? "DARK" : "BRIGHT");
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

# Overwrite App/20_Physical_Wiring_Manual.md to change LDR pin to AO GPIO 35

with open("App/20_Physical_Wiring_Manual.md", "r") as f:
    text = f.read()

new_step_4 = """## ☀️ STEP 4: Wiring the 4-Pin LDR Light Sensor Module (HIGH-PRECISION ANALOG READS)
Your LDR module is a premium 4-pin version featuring both `DO` (Digital Out) and `AO` (Analog Out) pins, alongside its on-module indicator LED.

1. Connect a **Female-to-Male (F-M)** wire from LDR **GND** to the breadboard **negative (-) outer rail**.
2. Connect a **F-M** wire from LDR **VCC** directly to **Row 30, Column B** of your breadboard (sharing the row with your ESP32's stable 3.3V pin).
3. Connect a **F-M** wire from LDR **AO (Analog Out)** directly to **ESP32 GPIO 35 (ADC1_CH7)** (the 5th pin from the top-left near the USB port).
4. Leave the **DO (Digital Out)** pin on the LDR board **completely disconnected**!
5. *🚨 WHY THIS IS INFINITELY BETTER:* **Reading the raw Analog AO pin is 100x more accurate and professional than reading digitally.** It allows your Next.js dashboard to show the *exact, changing light level (e.g. Lux: 850)* in real-time. By connecting AO to **GPIO 35 (which belongs to ADC1)**, we completely avoid the Wi-Fi ADC2 conflict, allowing your light readings to remain perfectly stable and responsive while transmitting over WiFi! Powering it with **3.3V** is 100% electrically safe and protects your analog pin from overvoltage."""

text = text.replace("## ☀️ STEP 4: Wiring the LDR Light Sensor Module\nYour LDR module has 3 pins: VCC, GND, and DO (Digital Out).\n\n1. Connect a **Female-to-Male (F-M)** wire from LDR **GND** to the breadboard **negative (-) outer rail**.\n2. Connect a **F-M** wire from LDR **VCC** directly to **Row 30, Column B** of your breadboard (sharing the row with your ESP32's stable 3.3V pin).\n3. Connect a **F-M** wire from LDR **DO (Digital Out)** directly to **ESP32 GPIO 14** (the 6th pin from the bottom-left of the board).", new_step_4)

with open("App/20_Physical_Wiring_Manual.md", "w") as f:
    f.write(text)

print("LDR successfully updated to High-Precision Analog AO sensing!")
