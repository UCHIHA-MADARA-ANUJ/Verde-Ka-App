# Project Verde V3.0 — ESP32-CAM Complete Testing Suite
### Master Test Guide for Local SD Saving and Wireless Direct HTTP Uploads

Aarav and Anuj, testing the **ESP32-CAM** (the "big guns" of your project) is the most exciting milestone! To ensure you get 100% successful results with zero errors, we have designed **two testing methodologies** that you can run right now:

1. **Way A: Local Capture & Save to SD Card (MicroSD/TF Card)**
   * *Purpose:* Tests the camera lens, resolutions, and local memory writing without requiring any WiFi or servers.
2. **Way B: Standalone Wireless HTTP Upload (Direct Stream to Laptop)**
   * *Purpose:* Tests the wireless WiFi transceiver and streams raw image bytes directly to a local Python server running on your laptop. **This is identical to how it will upload to your Next.js Vercel cloud!**

---

## 🔌 1. Mounting the ESP32-CAM onto the MB Shield

Before plugging anything in, look closely at how the ESP32-CAM sits on the **MB USB Programmer Shield**:
1. Slide the ESP32-CAM board directly into the female headers of the MB shield.
2. **Double-check alignment:** Ensure the **OV2640 camera lens is pointing OUTWARD** (away from the Micro-USB port of the shield).
3. The small reset button on the ESP32-CAM should align near the edge of the board.
4. Plug your Type-C or Micro-USB cable into the **Programmer Shield**, and connect it to your laptop's USB port.

---

## 💾 WAY A: Local Capture & Save to SD Card

To run this test, insert any **FAT32-formatted MicroSD card** (up to 32GB) into the metal SD card slot on the underside of your ESP32-CAM.

### 1. Arduino IDE Board Selection:
* **Board:** Select **`AI Thinker ESP32-CAM`** (under Tools -> Board -> esp32).
* **Port:** Select your active **COM Port** (COM7 or similar).
* **Upload Speed:** Set to `115200` (safer for ESP32-CAM).

### 2. The SD-Card Test Code:
Copy-paste this code into a new sketch in your Arduino IDE and click **Upload**:

```cpp
#include "esp_camera.h"
#include "Arduino.h"
#include "FS.h"                // File System library
#include "SD_MMC.h"            // SD Card library for ESP32-CAM
#include "soc/soc.h"           // Disable brownout problems
#include "soc/rtc_cntl_reg.h"

// AI-Thinker ESP32-CAM Camera Pinout Configuration
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

int pictureNumber = 0;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout detector
  Serial.begin(115200);

  // Initialize Camera
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
  
  config.frame_size = FRAMESIZE_SVGA; // 800x600 resolution (optimal for test)
  config.jpeg_quality = 10;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera initialization failed! Error: 0x%x\n", err);
    return;
  }

  // Initialize SD Card
  Serial.println("Initializing SD Card...");
  if(!SD_MMC.begin()){
    Serial.println("SD Card Mount Failed! Please format SD to FAT32.");
    return;
  }
  
  uint8_t cardType = SD_MMC.cardType();
  if(cardType == CARD_NONE){
    Serial.println("No SD Card attached!");
    return;
  }

  // 3. Take a Picture
  Serial.println("Taking snapshot...");
  camera_fb_t * fb = esp_camera_fb_get();  
  if(!fb) {
    Serial.println("Camera capture failed!");
    return;
  }
  
  // Create filename (e.g., /picture1.jpg)
  pictureNumber++;
  String path = "/picture" + String(pictureNumber) + ".jpg";

  fs::FS &fs = SD_MMC;
  Serial.printf("Saving picture to path: %s\n", path.c_str());

  File file = fs.open(path.c_str(), FILE_WRITE);
  if(!file){
    Serial.println("Failed to open file in write mode!");
  } 
  else {
    file.write(fb->buf, fb->len); // Write image bytes from RAM to SD
    Serial.printf("Saved successfully! Size: %d bytes\n", fb->len);
  }
  file.close();
  
  esp_camera_fb_return(fb); // Clear image from memory
  
  // Flash the onboard white LED briefly to signal success
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  delay(500);
  digitalWrite(4, LOW);
  
  Serial.println("Setup Complete. Unplug SD card and view photos on your laptop!");
}

void loop() {
  // Do nothing in loop
}
```

---

## 🌐 WAY B: Standalone Wireless HTTP Upload (Direct to Laptop)

In this test, your ESP32-CAM will connect to your phone's Wi-Fi hotspot and **send a captured photo wirelessly to a Python script running on your laptop**. 

### 1. Find Your Laptop's IP Address:
1. Connect both your laptop and your phone hotspot together.
2. On your laptop, open **Command Prompt** (cmd) and type: `ipconfig`
3. Look for the row that says **IPv4 Address** under your Wi-Fi adapter (it will look like `192.168.x.x` or `172.20.x.x`). **Note this down!**

### 2. Start the Local Python Server on Your Laptop:
Since you have a terminal environment on Replit/Workspace, we can create a lightweight receiver script. 
I have created a python script named **`local_receiver.py`** in your workspace. You can run it on your own Windows/Mac laptop by installing Flask (`pip install Flask`) and running it:

```python
# Save this on your laptop as: local_receiver.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get raw binary image data from the ESP32-CAM request body
        image_data = request.data
        if image_data:
            with open("uploaded_test.jpg", "wb") as f:
                f.write(image_data)
            print("🎉 Success! Image received and saved as 'uploaded_test.jpg'!")
            return "SUCCESS", 200
        else:
            print("⚠️ Received empty data packet.")
            return "EMPTY_DATA", 400

if __name__ == '__main__':
    # Starts server on port 5000, listening to all local network IPs
    app.run(host='0.0.0.0', port=5000)
```

### 3. Upload This Wireless Test Code to the ESP32-CAM:
Change `YOUR_WIFI_SSID`, `YOUR_WIFI_PASSWORD`, and `YOUR_LAPTOP_IP_ADDRESS` in this code, then upload it:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define LAPTOP_IP "YOUR_LAPTOP_IP_ADDRESS" // e.g., "192.168.43.45"

// AI-Thinker Camera Pinout
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
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout resets
  Serial.begin(115200);

  // Initialize Camera
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

  config.frame_size = FRAMESIZE_SVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x\n", err);
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");

  // Take photo and upload immediately
  captureAndUpload();
}

void loop() {
  // Do nothing in loop
}

void captureAndUpload() {
  Serial.println("Capturing photo...");
  camera_fb_t * fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("Capture failed!");
    return;
  }

  Serial.println("Uploading photo to laptop...");
  HTTPClient http;
  
  // Construct the local POST endpoint URL
  String serverUrl = "http://" + String(LAPTOP_IP) + ":5000/upload";
  http.begin(serverUrl);
  http.addHeader("Content-Type", "image/jpeg");

  int httpResponseCode = http.POST(fb->buf, fb->len); // POST raw bytes
  if (httpResponseCode > 0) {
    Serial.printf("POST Successful! Response Code: %d\n", httpResponseCode);
  } else {
    Serial.printf("POST Failed! Error: %s\n", http.errorToString(httpResponseCode).c_str());
  }
  
  http.end();
  esp_camera_fb_return(fb); // Free memory buffer
  Serial.println("Upload complete. Check your laptop folder for 'uploaded_test.jpg'!");
}
```

---

This is your comprehensive dual-method testing blueprint! Give either of these codes a shot when your boards arrive, and you will be completely in control of the camera's visual features. 

Let me know which method you'd like to try first, and we can discuss the results! Ready to win DAV ACON 5!
