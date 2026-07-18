# Verde Tech V3.0 — Developer Handoff Documentation

Welcome to the official developer handoff documentation folder for **Project Verde V3.0 (Autonomous Plant OS)**. This folder contains the complete technical specifications, database architectures, and API designs required to build the web and mobile applications from scratch.

## 📂 Documentation Directory

1. **[00_Project_Overview.md](./00_Project_Overview.md):** Project goals, target users, and components.
2. **[01_System_Architecture.md](./01_System_Architecture.md):** High-level topology and block diagrams.
3. **[02_Application_Workflow.md](./02_Application_Workflow.md):** Step-by-step user-to-device workflows.
4. **[03_ESP32_Communication.md](./03_ESP32_Communication.md):** Telemetry payload specs and Wi-Fi reconnection models.
5. **[04_ESP32_CAM_Workflow.md](./04_ESP32_CAM_Workflow.md):** On-demand image capture, storage pipelines, and production routing.
6. **[05_Backend_Architecture.md](./05_Backend_Architecture.md):** Node.js/Next.js serverless route configuration.
7. **[06_Supabase_vs_Firebase.md](./06_Supabase_vs_Firebase.md):** Direct comparison and final architecture recommendation.
8. **[07_Database_Design.md](./07_Database_Design.md):** Schema design, index strategies, and document trees.
9. **[08_API_Design.md](./08_API_Design.md):** Full REST endpoint specifications and payload examples.
10. **[09_Authentication.md](./09_Authentication.md):** Sign-up, login, and session lifecycles.
11. **[10_Row_Level_Security.md](./10_Row_Level_Security.md):** Security policies and bucket permission rules.
12. **[11_Image_Handling.md](./11_Image_Handling.md):** Image compression, storage, and 15-day auto-delete TTL policies.
13. **[12_Offline_and_Error_Handling.md](./12_Offline_and_Error_Handling.md):** Hard-fault, network drop, and device offline recovery.
14. **[13_Notifications.md](./13_Notifications.md):** Alerts, push frameworks, and dry-run pump warnings.
15. **[14_UI_UX_Guidelines.md](./14_UI_UX_Guidelines.md):** UI theme, loading states, grids, and accessibility.
16. **[15_Project_Rules.md](./15_Project_Rules.md):** Strict constraints (no localhost, no exposed keys, secure envs).
17. **[16_Best_Practices.md](./16_Best_Practices.md):** Directory structure, naming conventions, and testing strategies.
18. **[17_Future_Improvements.md](./17_Future_Improvements.md):** AI crop matching, weather routing, and predictive analytics.
19. **[18_Development_Checklist.md](./18_Development_Checklist.md):** Modular, step-by-step developer implementation tasks.
20. **[99_AI_Developer_Master_Prompt.md](./99_AI_Developer_Master_Prompt.md):** The master bootstrap prompt to feed a brand-new AI session.

---

## 🛠️ Tech Stack Baseline
* **Frontend:** Next.js (App Router), Tailwind CSS, Framer Motion, Recharts.
* **Backend:** Next.js Serverless API Routes (Node.js runtimes).
* **Database/Sync:** Firebase Realtime Database (WebSocket sync).
* **Storage:** Firebase Cloud Storage (5GB Free tier, 15-Day TTL).
* **AI:** Plant.id API (Diagnosis) + Gemini 2.0 Flash API (Conversational Advisor).
