// =========================================================================
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
#define WIFI_SSID "YOUR_WIFI_HOTSPOT_NAME"       // Enter your phone hotspot name
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"   // Enter your hotspot password
#define FIREBASE_HOST "YOUR_PROJECT_ID.firebaseio.com" // Enter your Firebase RTDB URL (without http:// or https://)
#define FIREBASE_AUTH "YOUR_DATABASE_SECRET"   // Enter your Firebase Database Secret Key

// Next.js API route that receives raw binary JPEG data
#define UPLOAD_URL "https://verde-tech-proj.vercel.app/api/upload-photo"
// Must match CAM_UPLOAD_API_KEY set in Vercel env vars (x-api-key guard)
#define UPLOAD_API_KEY "YOUR_SECURE_CAM_KEY"

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
  
  Serial.println("Firebase RTDB sync active. Waiting for capture commands...");
  Serial.println("=========================================================");
}

// -------------------------------------------------------------------------
// 🔄 CAMERA TRIGGER POLLING LOOP (LISTEN & EXECUTE "ON APPEAL")
// -------------------------------------------------------------------------
void loop() {
  if (millis() - lastTriggerCheck > checkInterval) {
    lastTriggerCheck = millis();

    bool captureRequested = false;
    
    // Poll Firebase Realtime Database for the trigger flag
    if (Firebase.getBool(fbData, "/controls/capture_photo")) {
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
        Firebase.setBool(fbData, "/controls/capture_photo", false); // Clear flag in Firebase
        return;
      }

      Serial.println("Uploading photo wirelessly to Next.js App...");
      HTTPClient http;
      http.begin(UPLOAD_URL);
      http.addHeader("Content-Type", "image/jpeg");
      http.addHeader("x-api-key", UPLOAD_API_KEY); // Auth guard on the Vercel route!

      // Post raw binary image bytes directly over-the-air!
      int httpResponseCode = http.POST(fb->buf, fb->len);
      if (httpResponseCode > 0) {
        Serial.printf("Upload Successful! HTTP Response: %d\n", httpResponseCode);
        
        // Write the flag back to false in Firebase to tell the app the upload is complete!
        Firebase.setBool(fbData, "/controls/capture_photo", false);
      } else {
        Serial.printf("Upload failed! Error: %s\n", http.errorToString(httpResponseCode).c_str());
        Firebase.setBool(fbData, "/controls/capture_photo", false); // Clear flag anyway to reset state
      }
      
      http.end();
      esp_camera_fb_return(fb); // CRITICAL: Free RAM buffer immediately to prevent leaks!
      Serial.println("Capture complete! Returning to idle state.");
    }
  }
}
