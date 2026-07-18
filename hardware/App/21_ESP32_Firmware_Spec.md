# 21. ESP32 & ESP32-CAM Master Firmware Specification Manual
### High-Performance Real-Time Control & Edge-AI System Spec for Project Verde V3.0
### Target Exhibition: DAV ACON 5 IoT & Tech Competition

---

## 📁 SECTION 1: HARDWARE LAYER & PINOUT ALLOCATION

### A. Main Control Deck (ESP32 DevKit V1 30-Pin)
To ensure high stability, noise-immunity, and prevent internal hardware conflicts, the 30 pins of the ESP32 are mapped strictly to the following peripherals:

```
                          DOIT ESP32 DEVKIT V1 (30-PIN)
                                  TOP VIEW
                               +  [ USB ]  +
                     [EN]  [1] |           | [15] [VIN]  ──► Breadboard 5V (+)
          Moisture (AO) ◄─ [34] |           | [14] [GND]  ──► Breadboard GND (-)
               LDR (AO) ◄─ [35] |           | [13] [3V3]  ──► LDR & Moisture VCC
                           [32] |           | [12] [D15]
                           [33] |           | [11] [D2]
                           [25] |           | [10] [D4]   ──► DHT DATA
                           [26] |           | [9]  [RX2]  ──► GPIO 16
                           [27] |           | [8]  [TX2]  ──► GPIO 17
                           [14] |           | [7]  [D5]   ──► Relay IN1 (Pump)
               UV LED ◄─── [12] |           | [6]  [D18]  ──► HC-SR04 TRIGGER
                           [13] |           | [5]  [D19]  ──► HC-SR04 ECHO
              Relay IN2 ◄─ [23] |           | [4]  [D21]
          Gated Moisture ◄─ [22] |           | [3]  [D22]
          Power (VCC)      [GND]|           | [2]  [D23]
                               +───────────+
```

| Component | ESP32 GPIO | Channel Type | Hardware Details & Justification |
| :--- | :---: | :--- | :--- |
| **Water Pump Relay IN1**| **GPIO 5** | Digital Output | Optocoupler-isolated Active-Low trigger line. |
| **Spare Relay IN2** | **GPIO 23** | Digital Output | Active-Low trigger line reserved for system expansion. |
| **DHT11/DHT22 DATA** | **GPIO 4** | Digital Input | Single-bus digital data stream. |
| **Everlight 5mm UV LED**| **GPIO 12** | Digital Output | Active-High GPIO. Connects through a 220-Ohm current-limiting resistor to protect the pin from overcurrent. |
| **Soil Moisture (AO)** | **GPIO 34** | Analog Input | **ADC1_CH6:** Sits on Analog-to-Digital Converter 1. Safe from Wi-Fi conflicts. |
| **Moisture Gated VCC** | **GPIO 22** | Digital Output | Gated power switch. Fired HIGH (3.3V) for 15ms during reads, then pulled LOW to prevent electrolysis. |
| **LDR Analog Out (INV)**| **GPIO 35** | Analog Input | **ADC1_CH7:** Sits on ADC1. Safe from Wi-Fi conflicts. |
| **HC-SR04 TRIGGER** | **GPIO 18** | Digital Output | Sends 10-microsecond trigger pulse. |
| **HC-SR04 ECHO** | **GPIO 19** | Digital Input | Reads returned sound wave duration using `pulseIn()`. |

### B. Standalone Camera Node (AI-Thinker ESP32-CAM)
The ESP32-CAM operates completely independently on its own MB Programmer Shield:
* **Camera Sensor:** OV2640 2MP lens module connected via the on-board DVP parallel bus.
* **On-Board Flash LED:** Connected internally to **GPIO 4**. 
* **Power:** Powered independently via a dedicated USB-C cable from your laptop, a phone charger, or a USB power bank.

---

## ⚡ SECTION 2: SYSTEM STATE MACHINE (MANUAL vs. AUTO COORDINATION)

The system operates as a state machine with two highly distinct, switchable execution profiles:

```
                           +─────────────────────────+
                           |      SYSTEM STARTUP     |
                           +─────────────────────────+
                                        │
                                        ▼
                           +─────────────────────────+
                           |  Firebase Handshake     |
                           +─────────────────────────+
                                        │
                                        ▼
                           +─────────────────────────+
                           |  Poll "/controls/Mode"  |
                           +─────────────────────────+
                                  /                                  Mode="AUTO"             Mode="MANUAL"
                             /                                                 ▼                       ▼
               +────────────────────────+     +────────────────────────+
               |    AUTONOMOUS MODE     |     |      MANUAL MODE       |
               |                        |     |                        |
               |  - Reads moisture %    |     |  - Reads app state for |
               |  - If < threshold:     |     |    /controls/pump_state|
               |    PUMP ON             |     |    and grow_light_state|
               |  - If LDR < 400 Lux:   |     |                        |
               |    UV LED ON           |     |  - Fires relays/LEDs   |
               |  - Obey Rain Override  |     |    on direct demand    |
               +────────────────────────+     +────────────────────────+
```

### A. Manual Mode Execution Profile
* **Trigger:** The app sets `/controls/manual_mode = true`.
* **State Behavior:**
  * The ESP32 completely disables its autonomous threshold comparison algorithms.
  * It polls `/controls/pump_state` and `/controls/grow_light_state` over WebSockets.
  * If `pump_state == true`, it pulls **GPIO 5 LOW (ON)**. If `false`, it pulls **GPIO 5 HIGH (OFF)**.
  * If `grow_light_state == true`, it pulls **GPIO 12 HIGH (ON)**. If `false`, it pulls **GPIO 12 LOW (OFF)**.
  * This allows the user to turn on/off the pump and grow lights individually and on-demand from the Next.js app!

### B. Autonomous Mode Execution Profile
* **Trigger:** The app sets `/controls/manual_mode = false`.
* **State Behavior:**
  * The ESP32 reads the local soil moisture percentage. If it falls below `/controls/moisture_threshold` (default 30%), it triggers the pump ON.
  * **The Rain Override:** If `/controls/weather_override == 1` (meaning Anuj's OpenWeatherMap script detected rain in Delhi), **irrigation is immediately suspended**, even if the soil is dry!
  * **The Light Loop:** The ESP32 reads LDR Lux. If Lux falls below 400, it automatically turns the 5mm UV LED ON and writes `/controls/grow_light_state = true` to Firebase so your app dashboard updates its indicator widget in real-time.

---

## 📏 SECTION 3: SENSOR MATHEMATICS & CALIBRATION

### A. Water Reservoir Depth-to-Percentage Calculation (HC-SR04)
The ultrasonic sensor sits face-down on the bucket lid. It measures the distance to the water surface.

```
       [ HC-SR04 Sensor ]  ◄── Mounted on Lid
      |──────────────────|
      |   (TRIG) (ECHO)  |
      +──────────────────+
        │              ▲
        │ Sound Pulse  │ Echo Return
        ▼              │
    ~~~~~~~~~~~~~~~~~~~~~~ ◄── Water Surface (Distance 'D')
    |                    |
    |                    |
    |                    | ◄── Bucket Depth (Max: 18cm, Min: 2cm)
    +────────────────────+ ◄── Bucket Bottom
```

#### 1. The Physics Math:
* Speed of sound in air = $340 	ext{ m/s} = 0.034 	ext{ cm/}\mu	ext{s}$.
* Since the pulse travels to the water surface and back, the one-way distance ($D$) is:
  $$D = rac{	ext{Echo Duration in Microseconds} 	imes 0.034}{2}$$

#### 2. Converting Distance to Percentage (0% to 100%):
* Let's calibrate your bucket:
  * **Bucket is Empty (0%):** The water level is at the bottom, so the distance to the sensor is maximum, say **18 cm**.
  * **Bucket is Full (100%):** The water level is close to the top, so the distance to the sensor is minimum, say **2 cm** (never submerge the sensor!).
* The mapping formula:
  $$	ext{TankLevel \%} = rac{(18 - D)}{(18 - 2)} 	imes 100$$
* In C++ code:
  ```cpp
  float distance = duration * 0.034 / 2;
  int tankLevelPct = map(distance, 18, 2, 0, 100);
  tankLevelPct = constrain(tankLevelPct, 0, 100); // Prevents out-of-range readings
  ```

#### 3. Edge Cases & Failure Recovery:
* **Edge Case: Water level overflows (> 100%):** If water comes closer than 2cm, the percentage would calculate above 100%. The `constrain()` function caps this at exactly `100`.
* **Edge Case: Out-of-Range Echo (No reflection):** If the sensor receives no echo (sound absorbed or sensor tilted), `pulseIn()` returns `0`. This would calculate as a false 100% full tank.
  * **The Failsafe:** If `duration == 0`, mark `tankLevelPct = 0` and trigger an alert flag to prevent pump dry-runs.

---

## 📷 SECTION 4: ESP32-CAM ON-DEMAND UPLOAD PIPELINE

To prevent your camera from drawing high continuous current, it operates strictly **on-demand (on appeal)**:

### A. The Wireless Handshake Flow
1. The camera boots up, connects to WiFi, and polls Firebase `/controls/capture_photo` every 2 seconds.
2. The user clicks **"Scan Foliage"** on the Next.js app. The app sets `capture_photo = true` in Firebase RTDB.
3. The camera reads the true flag:
   * It pulls **GPIO 4 HIGH** to turn on the bright white flash.
   * It waits 150ms for the light to stabilize, then snaps a JPEG frame.
   * It pulls **GPIO 4 LOW** to turn the flash OFF immediately.
4. The camera makes an HTTP POST request to Anuj's Next.js Vercel API:
   `https://verde-tech-proj.vercel.app/api/upload-photo`
5. **The Server-Side Reset:** 
   * Vercel receives the raw binary bytes, uploads the JPEG file to Firebase Storage, and **automatically writes `/controls/capture_photo = false` back to Firebase RTDB**.
   * This immediately stops the loading spinner on the user's dashboard!
6. **The Memory Safeguard:** Once the POST request completes, the ESP32-CAM runs **`esp_camera_fb_return(fb);`** to completely free the frame buffer RAM, preventing memory leaks and crashes.
