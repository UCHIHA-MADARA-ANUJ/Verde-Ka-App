"use client";
// ============================================================
// LANDING — cinematic splash with animated entry into the deck.
// ============================================================
import Link from "next/link";
import { motion } from "framer-motion";
import { Sprout, ChevronRight, Cpu, Camera, Database, Bot } from "lucide-react";

const FEATURES = [
  { icon: Cpu, label: "ESP32 EDGE BRAIN", sub: "5 sensors · 2 actuators · 4s telemetry" },
  { icon: Database, label: "REALTIME SYNC", sub: "Firebase WebSocket · <100ms" },
  { icon: Camera, label: "VISION NODE", sub: "On-demand foliage scans · 8MHz CAM" },
  { icon: Bot, label: "AI BOTANIST", sub: "Plant.id + Gemini 2.0 Flash" },
];

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6">
      {/* Ambient grid backdrop */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(34,197,94,0.4) 1px, transparent 1px), linear-gradient(90deg, rgba(34,197,94,0.4) 1px, transparent 1px)",
          backgroundSize: "42px 42px",
        }}
      />
      {/* Glow orb */}
      <motion.div
        className="pointer-events-none absolute h-[500px] w-[500px] rounded-full"
        style={{
          background:
            "radial-gradient(circle, rgba(34,197,94,0.12) 0%, transparent 65%)",
        }}
        animate={{ scale: [1, 1.15, 1] }}
        transition={{ duration: 5, repeat: Infinity }}
      />

      <div className="relative z-10 w-full max-w-3xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-verde-green/30 bg-verde-green/5 px-4 py-1.5 text-[9px] tracking-[0.3em] text-verde-dim">
            <Sprout size={11} className="text-verde-green" />
            DAV ACON 5 · TECH EXHIBITION · DELHI
          </div>

          <h1 className="text-5xl tracking-[0.25em] text-verde-green sm:text-7xl">
            <motion.span
              animate={{
                textShadow: [
                  "0 0 25px rgba(34,197,94,0.5)",
                  "0 0 55px rgba(34,197,94,0.9)",
                  "0 0 25px rgba(34,197,94,0.5)",
                ],
              }}
              transition={{ duration: 2.5, repeat: Infinity }}
            >
              VERDE
            </motion.span>
          </h1>
          <p className="mt-3 text-xs tracking-[0.5em] text-verde-text sm:text-sm">
            AUTONOMOUS PLANT OS · V3.0
          </p>
          <p className="mx-auto mt-5 max-w-lg text-[11px] leading-relaxed text-verde-muted">
            Industrial-grade smart garden: remote irrigation, live telemetry,
            weather-aware watering, and AI-powered leaf disease diagnostics —
            from anywhere on Earth.
          </p>
        </motion.div>

        {/* Feature chips */}
        <div className="mt-10 grid grid-cols-2 gap-3 md:grid-cols-4">
          {FEATURES.map((f, i) => {
            const Icon = f.icon;
            return (
              <motion.div
                key={f.label}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + i * 0.1 }}
                className="crt relative rounded-lg border border-verde-border bg-verde-panel/70 p-4 backdrop-blur transition-all duration-200 hover:border-verde-green/40 hover:shadow-glow"
              >
                <Icon size={16} className="mx-auto mb-2 text-verde-green" />
                <p className="text-[9px] tracking-widest text-verde-text">
                  {f.label}
                </p>
                <p className="mt-1 text-[8px] leading-relaxed text-verde-muted">
                  {f.sub}
                </p>
              </motion.div>
            );
          })}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-10"
        >
          <Link
            href="/dashboard"
            className="group inline-flex items-center gap-2 rounded border border-verde-green bg-verde-green/10 px-8 py-4 text-sm tracking-widest text-verde-green transition-all duration-300 hover:bg-verde-green/20 hover:shadow-glow-lg"
          >
            ENTER CONTROL DECK
            <ChevronRight
              size={16}
              className="transition-transform group-hover:translate-x-1"
            />
          </Link>
          <p className="mt-6 text-[8px] tracking-[0.3em] text-verde-muted">
            BUILT BY AARAV & ANUJ · ESP32 WROOM-32 + ESP32-CAM · FIREBASE RTDB
          </p>
        </motion.div>
      </div>
    </main>
  );
}
