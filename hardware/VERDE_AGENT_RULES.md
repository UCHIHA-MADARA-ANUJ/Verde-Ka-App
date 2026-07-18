# Verde Tech V3.0 — Core Agent Directives & Rules
### Protocol for Any AI Agent Accessing This Workspace

Welcome, Agent. You are entering the workspace of **Project Verde V3.0 (Smart IoT Irrigation & Plant Care System)** designed for the **DAV ACON 5 Tech Exhibition**. 

You are required to follow these core instructions, design standards, and execution loops to maintain elite professionalism and keep the project at a **100/100** score.

---

## 🚦 1. Core Agent Directives

1. **Read Before You Build:** Before executing any task, read **`VERDE_PROJECT_LOGBOOK.md`** and **`Verde_Tech_V3_Blueprint.md`** in this workspace to understand current hardware pinouts, databases, and physical constraints. Do not duplicate or contradict existing assignments.
2. **The "Plan-Review-Perfect" (PRP) Loop:** 
   * **Plan:** Meticulously outline the solution first. Identify parameters, potential bugs, and library compatibility.
   * **Make:** Write clean, modular, and highly commented code (either Next.js frontend, Node.js API, or ESP32 C++ firmware).
   * **Review:** Audit your code. Check for edge-case errors (such as offline database states, memory overflow, sensor timeouts, and syntax errors).
   * **Iterate:** Refine and perfect the code repeatedly until there are **zero bugs**.
3. **Keep the Logbook Updated:** After completing your prompt response, update **`VERDE_PROJECT_LOGBOOK.md`** with a quick summary of what was implemented, current state of files, and next-step priorities. This ensures seamless model-switching.

---

## 🎨 2. Digital UI/UX & Web Design Standards (Pro Max)

When developing the Next.js web application or dashboard, apply these professional frontend guidelines:

* **Cyberpunk / Minimal Terminal Aesthetic:** Stick to the dark-theme brand of Verde: deep dark grays/blacks, glowing green highlights (`rgb(34,197,94)`), clear border lines, and micro-grid layouts.
* **Responsive Layouts:** Everything must be fully responsive using Tailwind CSS (`grid-cols-1 md:grid-cols-2 lg:grid-cols-4`).
* **Motion & Animations:** Use smooth transitions and state-based animations. If required, utilize **GSAP** (GreenSock Animation Platform) or **Framer Motion** for premium interactive scroll animations.
* **Data Visualization:** Use high-performance libraries like **Chart.js** or **Recharts** to plot live sensor data feeds smoothly with glowing green area gradients under the charts.
* **User Experience (UX) Feedback:** Buttons must show immediate active/loading states, manual triggers must have instant-feedback spinners, and warning banners (like low water bucket level) must pulse gently.

---

## ⚡ 3. Embedded Systems & C++ Code Standards

When writing firmware for the ESP32 main controller or the ESP32-CAM:

* **Hardware Serial Only:** Use hardware serial ports (`Serial2` on pins 16 & 17) for peripheral modules. Never use SoftwareSerial on ESP32 as it causes processor blocks.
* **Non-Blocking Logic:** Do not use `delay()` in main loops. Use `millis()`-based task scheduling so the board can poll Firebase, read sensors, and listen to manual overrides without lagging.
* **Power Stability & Protection:** Meticulously account for voltage sags and back-EMF spikes. Always utilize decoupling capacitors and flyback diodes across inductive loads like water pumps.
* **Power Gating for Soil Probes:** To stop electrolysis and corrosion on 2-prong resistive moisture sensors, keep the sensor's VCC connected to a digital GPIO pin, turning it HIGH only during a 10ms read window and pulling it LOW immediately after.

---

## 🔗 4. External Integrations (Figma MCP & Open Source)

* **Figma Connection:** If a Figma MCP (Model Context Protocol) is connected, search the frames for `Verde Tech Dashboard V3` to extract exact hex colors, padding, and layout geometries.
* **3D Models:** Utilize open-source STL links for 3D printed housings or custom mounting rigs. Keep mechanical prints minimal and functional.
