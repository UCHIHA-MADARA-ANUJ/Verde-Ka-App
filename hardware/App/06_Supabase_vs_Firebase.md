# 06. Supabase vs. Firebase Comparison

This document provides a professional, deep architectural comparison between **Firebase Realtime Database** and **Supabase (PostgreSQL)** for the execution of our smart garden IoT prototype.

---

## 📊 1. Face-to-Face Technical Comparison

| Feature Metric | Firebase (Realtime Database) | Supabase (PostgreSQL) |
| :--- | :--- | :--- |
| **Real-Time Latency** | WebSocket-based native sync (**<100ms**). | Realtime triggers on Postgres WAL. |
| **Microcontroller Support**| Lightweight, highly stable `Firebase-ESP32` SDK. | Complex manual REST/JWT header assembly. |
| **Storage Allocation** | **5 GB** completely free. | **1 GB** completely free. |
| **Database Rules** | Simple JSON paths, extremely easy to audit. | SQL-based Row Level Security (RLS) policies. |
| **Data Format** | Single JSON Document Tree. | Relational SQL Tables & Foreign keys. |
| **Authentication** | Built-in Anonymous & Email Auth. | GoTrue Go-based Auth schemas. |

---

## 🏆 2. Architectural Recommendation: Firebase RTDB

**Firebase Realtime Database (RTDB) is selected as the database of choice.**

### Deep Technical Justifications:
1. **Processor Overhead & Memory Constraints:** The ESP32 is a low-power microcontroller. Running a SQL-based ORM or assembling complex HTTP POST headers with JWT authorization strings for Supabase's Postgres API uses significant RAM, leading to **heap allocation failures** and crashes. The Mobizt `FirebaseESP32` client handles SSL/TLS handshakes internally with extreme stability.
2. **Sub-100ms Manual Toggles:** Firebase RTDB holds a persistent, open WebSocket stream with the ESP32. When you click "Force ON" on the app, the state change travels over the air and triggers the pump relay in **less than 100ms**. Supabase’s PostgreSQL real-time engine, while robust, introduces several database layers (Write-Ahead Log listener -> realtime server -> client), resulting in higher latency and slower, clunky physical responses during live demos.
3. **Generous Storage Free Tier:** Firebase offers **5 GB** of cloud storage completely free, which is 5x larger than Supabase's 1 GB free tier. This allows you to store thousands of leaf scans without running out of space!
