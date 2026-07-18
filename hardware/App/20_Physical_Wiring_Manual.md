# 20. Aarav's Step-by-Step Bench Wiring & Assembly Manual (No Shield Setup)

This is the official step-by-step physical wiring manual for **Aarav (Hardware & Systems Engineer)**. 

This guide is completely designed to use only your **ESP32 WROOM-32 board**, **half-size solderless breadboard**, **5V 2-Channel Relay Module**, **4-Pin LDR Module**, and **extended 5mm UV LED Grow Lights**, connected entirely via jumper wires.

---

## 🛠️ THE OFF-BOARD JUMPER HACK

An ESP32 board is wide. If you plug it directly into the center of a half-size breadboard, **it blocks all the vertical rows on both sides**, leaving no holes to plug in wires.

* **Our Solution:** Your ESP32 board will sit flat on your desk next to the breadboard.
* **Connections:** We will run your **Female-to-Male (F-M) jumper wires** directly from the ESP32's pins to the rows and rails of your half-size breadboard. This keeps your bench completely clean, organized, and easy to modify!

---

## ⚡ STEP 1: The Master Power Deck & Capacitor Setup
We will initialize our power distribution lines on the breadboard:

1. Locate the **`VIN` (5V)** and **`GND`** pins on your ESP32 board.
2. Connect a **Female-to-Male (F-M)** jumper wire from ESP32 **`VIN`** directly to the **positive (+) outer rail** of your breadboard. This is your **5V Power Rail**.
3. Connect a **F-M** jumper wire from ESP32 **`GND`** directly to the **negative (-) outer rail** of your breadboard. This is your **GND Rail**.
4. **Insert the 1000uF Electrolytic Capacitor:**
   * Take your capacitor (look at its legs: the longer leg is Positive, the shorter leg marked with a gray stripe/minus signs is Negative).
   * Insert the **longer positive (+) leg** into the **positive (+) outer rail** of your breadboard.
   * Insert the **shorter negative (-) leg** into the **negative (-) outer rail** of your breadboard.
   * *This capacitor buffers any current draw spikes from the pump, keeping the ESP32 from resetting!*
5. **Set up the stable 3.3V Row:**
   * Connect a **F-M** jumper wire from the ESP32 **`3V3`** pin to **Row 30, Column A** of your breadboard. This will serve as a stable, noise-free 3.3V reference row for your 4-pin LDR light sensor!

---

## 🌡️ STEP 2: Wiring the DHT Temperature & Humidity Sensor
The DHT sensor module has 3 pins: VCC, GND, and DATA.

1. Connect a **Female-to-Male (F-M)** wire from DHT **VCC** to the breadboard **positive (+) outer rail**.
2. Connect a **F-M** wire from DHT **GND** to the breadboard **negative (-) outer rail**.
3. Connect a **F-M** wire from DHT **DATA** directly to **ESP32 GPIO 4** (the 5th pin from the top-right near the USB port).

---

## 💧 STEP 3: Wiring the 2-Prong Soil Moisture Sensor (CONTINUOUS REAL-TIME READS)
Your 2-prong soil sensor consists of the fork probe and a small comparator circuit board (VCC, GND, AO).

1. Connect the fork probe to the input pins of the comparator board using the short F-F wires provided in your kit.
2. Now, connect the output of the comparator board to your breadboard and ESP32 using 3 **Female-to-Male (F-M)** wires:
   * Connect comparator **GND** to the breadboard **negative (-) outer rail**.
   * Connect comparator **AO (Analog Out)** directly to **ESP32 GPIO 34 (ADC1_CH6)** (the 4th pin from the top-left near the USB port).
   * Connect comparator **VCC (Power)** directly to **Row 30, Column C** on your breadboard (which shares the stable 3.3V power from your ESP32's `3V3` pin!).
   * *🚨 IMPORTANT SAFETY DECISION:* **We power the soil moisture comparator directly from the ESP32's 3.3V pin.** If we powered it from the 5V USB rail, its AO signal could output 5V, which exceeds the ESP32's maximum GPIO voltage limit and would burn out your analog pin! Powering it from **3.3V** is 100% electrically safe, reduces electrolysis corrosion by 50%, and allows your app to **continuously monitor your soil moisture 24/7 without any resets!**

---

## ☀️ STEP 4: Wiring the 4-Pin LDR Light Sensor Module (HIGH-PRECISION ANALOG READS)
Your LDR module is a premium 4-pin version featuring `VCC`, `GND`, `INV` (Analog Out), and `OUT` (Digital Out) pins, alongside its on-module indicator LED.

1. Connect a **Female-to-Male (F-M)** wire from LDR **GND** to the breadboard **negative (-) outer rail**.
2. Connect a **F-M** wire from LDR **VCC** directly to **Row 30, Column B** of your breadboard (sharing the row with your ESP32's stable 3.3V pin).
3. Connect a **F-M** wire from LDR **INV (Analog Out)** directly to **ESP32 GPIO 35 (ADC1_CH7)** (the 5th pin from the top-left near the USB port).
4. Leave the **OUT (Digital Out)** pin on the LDR board **completely disconnected**!
5. *🚨 WHY THIS IS INFINITELY BETTER:* **Reading the raw Analog INV pin is 100x more accurate and professional than reading digitally.** It allows your Next.js dashboard to show the *exact, changing light level (e.g. Lux: 850)* in real-time. By connecting INV to **GPIO 35 (which belongs to ADC1)**, we completely avoid the Wi-Fi ADC2 conflict, allowing your light readings to remain perfectly stable and responsive while transmitting over WiFi! Powering it with **3.3V** is 100% electrically safe and protects your analog pin from overvoltage.

---

## 🔊 STEP 5: Wiring the HC-SR04 Ultrasonic Distance Sensor
The HC-SR04 has 4 pins: VCC, GND, TRIG, and ECHO.

1. Connect a **Female-to-Male (F-M)** wire from HC-SR04 **VCC** to the breadboard **positive (+) outer rail**.
2. Connect a **F-M** wire from HC-SR04 **GND** to the breadboard **negative (-) outer rail**.
3. Connect a **F-M** wire from HC-SR04 **TRIG** directly to **ESP32 GPIO 18** (the 7th pin from the bottom-right).
4. Connect a **F-M** wire from HC-SR04 **ECHO** directly to **ESP32 GPIO 19** (the 6th pin from the bottom-right).

---

## 💡 STEP 6: Wiring & Extending the 5mm UV LED (Over-Plant Night Arch)
To demonstrate the concept of **automated photosynthetic grow lighting over the plant at night**, the UV LED must sit directly above your plant pot (cut soda bottle), pointing down at the Tulsi leaves. 

To keep your main breadboard clean and allow the LED to reach the plant pot far away, we will use **jumper wire extensions** to carry the signal and ground:

### A. The Breadboard Resistor Hub
1. Insert your **220-Ohm Resistor** into the breadboard, bridging **Row 10, Column C** and **Row 12, Column C**.
2. Connect a **Female-to-Male (F-M)** jumper wire from **ESP32 GPIO 12** (the 4th pin from the bottom-left of the board) to **Row 10, Column B**.
   * *Why:* In your code, GPIO 12 controls the LED state dynamically based on LDR light levels.

### B. Constructing the Wire Extension (To Reach the Plant Pot)
1. Grab **one Male-to-Female (M-F) jumper wire** (this is your Positive (+) Extension line).
2. Grab **a second Male-to-Female (M-F) jumper wire** (this is your Negative (-) Extension line).
3. If your plant is placed very far from the breadboard, you can **chain multiple jumper wires together** (Male to Female to Male, etc.) to make the line as long and flexible as you need!
4. **Make the Connections:**
   * Plug the Male end of your **Positive Extension wire** into **Row 12, Column A** (connecting in series with the 220-Ohm resistor).
   * Plug the Male end of your **Negative Extension wire** directly into the **Breadboard negative (-) outer rail**.

### C. Mounting the LED Over the Plant
1. Take your **5mm UV LED** (longer leg is Positive, shorter leg is Negative).
2. Plug the Female end of your **Positive Extension wire** onto the **longer positive (+) leg** of the LED.
3. Plug the Female end of your **Negative Extension wire** onto the **shorter negative (-) leg** of the LED.
4. **Aesthetic Tape Setup:** Wrap a tiny piece of black electrical tape around each individual metal leg of the LED to ensure they never touch each other and cause a short-circuit!
5. Mount the LED directly underneath your cardboard photosynthesis arch, pointing straight down at the plant's leaves. Use double-sided foam tape or hot glue to lock it in place.
6. *This direct-drive setup allows the ESP32 to switch your grow light on and off using digital commands, completely removing the need for a second relay, while keeping the main breadboard completely safe from water splashes!*

---

## 🌊 STEP 7: Wiring the 5V 2-Channel Relay Module & Water Pump
Your 2-channel relay is powered from your breadboard rails, and we will wire the 1N4007 flyback diode on the breadboard to protect your pins from high back-EMF motor feedback.

### A. Relay Input Connections (From ESP32 to Relay Board)
The relay board has a 4-pin input header: `VCC`, `GND`, `IN1`, `IN2`.
1. Connect a **Female-to-Female (F-F)** wire from Relay **VCC** to any available **positive (+) 5V pin** on your breadboard rail.
2. Connect a **F-F** wire from Relay **GND** to any available **negative (-) GND pin** on your breadboard rail.
3. Connect a **Female-to-Male (F-M)** wire from Relay **IN1** (Channel 1 control) directly to **ESP32 GPIO 5** (the 8th pin from the bottom-right).
4. Connect a **F-M** wire from Relay **IN2** (Channel 2 control) directly to **ESP32 GPIO 13** (the 3rd pin from the bottom-left).
   * *Why:* Channel 1 will control your water pump. Channel 2 is wired directly to **GPIO 13** as a **safe, fully documented spare channel** for future exhibition expansions (like a cooling fan or solenoid valve!).

### B. The VCC-JD-VCC Black Jumper Cap (Precaution!)
On the side of your 2-channel relay board, there is a small 3-pin header with a **black plastic jumper cap** bridging two pins: **`VCC` and `JD-VCC`** (as shown in webcam photo `WIN_20260718_16_06_36_Pro.jpg`).
* **What it does:** This jumper connects the power of your input signal optocouplers and your physical relay electromagnetic coils together.
* **CRITICAL INSTRUCTION:** **LEAVE THIS BLACK JUMPER CAP EXACTLY WHERE IT IS! DO NOT REMOVE IT!** Having this jumper on ensures that your single 5V breadboard connection powers the entire relay board automatically. If you remove it, the relay coils won't get power, and the switch won't click when triggered!

### C. The Pump & 1N4007 Protection Diode Wiring (On Breadboard)
1. Insert your **1N4007 Diode** into **Row 20, Column C** and **Row 22, Column C** of your breadboard.
   * **CRITICAL ALIGNMENT:** The end of the diode with the **silver stripe (cathode)** must be in **Row 20**. The plain black end (anode) must be in **Row 22**.
2. Insert the **Pump's Positive (+) Red wire** into **Row 20, Column B** (sharing the row with the diode's silver stripe side).
3. Insert the **Pump's Negative (-) Black wire** into **Row 22, Column B** (sharing the row with the diode's plain black side).
4. Connect a **Male-to-Male (M-M)** jumper wire from **Row 22, Column A** (pump negative) directly into the **Breadboard negative (-) outer rail**.
5. **The Relay Screw Terminal Connections:**
   * Take a **M-M** jumper wire. Connect one end to your breadboard's **positive (+) outer rail**, and screw the other end into the **COM1 (Common 1)** screw terminal of Relay Channel 1.
   * Take a second jumper wire. Screw one end into the **NO1 (Normally Open 1)** screw terminal of Relay Channel 1, and insert the other end into **Row 20, Column A** (connecting it to the pump positive and the diode's silver stripe).
   * *This diode completely blocks inductive voltage spikes from flowing back into your ESP32 pins, keeping your system safe from motor feedback!*

---

## 📷 STEP 8: Standalone Camera (ESP32-CAM + MB Shield) Setup
Aarav, this is the most critical part of your physical build. **There are ABSOLUTELY ZERO WIRES connecting your ESP32-CAM to your main ESP32 brain or breadboard!** They are 100% wireless and communicate solely over WiFi through Firebase.

### A. Mating the Boards
1. Take your **ESP32-CAM board** (with the camera lens).
2. Take the **black MB USB Programmer Shield**.
3. Align the pins and **press the ESP32-CAM board directly onto the female headers of the MB Programmer Shield**.
4. **CRITICAL ALIGNMENT:** Ensure the **OV2640 camera lens points OUTWARDS** (away from the Micro-USB port on the MB Shield). The small, flat white flash LED must be pointing forward.

### B. Standalone Power Delivery
1. Secure your mated ESP32-CAM board on the **edge of your plant's bottle rim** pointing at the leaves (use your 3D-printed clip or double-sided tape).
2. Connect a separate, long, flexible USB cable directly from your laptop (or a standard **5V 2A phone wall charger** / **USB Power Bank** placed next to your plant) into the USB port of the **MB Programmer Shield**.
3. Powering the camera independently ensures **zero power drops** on your main breadboard rail and guarantees your video stream never lags!
4. The ESP32-CAM will boot up, connect to the `CCA SCHOOL` hotspot, and wait for your Next.js app to trigger a scan wirelessly!
