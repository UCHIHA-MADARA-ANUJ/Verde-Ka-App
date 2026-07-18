"use client";
// ============================================================
// LANDING — cinematic hero: perspective grid floor, floating
// spores, glitch title, staggered feature chips, glow CTA.
// ============================================================
import Link from "next/link";
import { motion } from "framer-motion";
import { Sprout, ChevronRight, Cpu, Camera, Database, Bot } from "lucide-react";

const FEATURES = [
  { icon: Cpu, label: "ESP32 EDGE BRAIN", sub: "5 sensors · 2 actuators · 4s telemetry" },
  { icon: Database, label: "REALTIME SYNC", sub: "Firebase WebSocket · <100ms" },
  { icon: Camera, label: "VISION NODE", sub: "On-demand foliage scans · 8MHz CAM" },
  { icon: Bot, label: "AI BOTANIST", sub: "crop.health + Gemini 2.5 Flash" },
];

function prand(i, salt) {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 py-16">
      {/* Perspective grid floor */}
      <div className="grid-floor pointer-events-none absolute inset-x-0 bottom-0 h-[45vh]" />

      {/* Floating spores */}
      {Array.from({ length: 18 }).map((_, i) => (
        <motion.span
          key={i}
          className="pointer-events-none absolute rounded-full bg-verde-green"
          style={{
            width: 2 + prand(i, 3) * 3,
            height: 2 + prand(i, 3) * 3,
            left: `${prand(i, 1) * 100}%`,
            top: `${prand(i, 2) * 100}%`,
            boxShadow: "0 0 8px rgba(34,197,94,0.8)",
          }}
          animate={{
            y: [0, -30 - prand(i, 4) * 40, 0],
            x: [0, (prand(i, 5) - 0.5) * 40, 0],
            opacity: [0.1, 0.7, 0.1],
          }}
          transition={{
            duration: 6 + prand(i, 6) * 8,
            repeat: Infinity,
            ease: "easeInOut",
            delay: prand(i, 7) * 4,
          }}
        />
      ))}

      {/* Center glow orb */}
      <motion.div
        className="pointer-events-none absolute h-[560px] w-[560px] rounded-full"
        style={{
          background:
            "radial-gradient(circle, rgba(34,197,94,0.14) 0%, transparent 65%)",
        }}
        animate={{ scale: [1, 1.18, 1], opacity: [0.8, 1, 0.8] }}
        transition={{ duration: 5, repeat: Infinity }}
      />

      <div className="relative z-10 w-full max-w-3xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.15 }}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-verde-green/30 bg-verde-green/5 px-4 py-1.5 text-[9px] tracking-[0.3em] text-verde-dim backdrop-blur"
          >
            <motion.span
              animate={{ rotate: [0, 12, -12, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <Sprout size={11} className="text-verde-green" />
            </motion.span>
            DAV ACON 5 · TECH EXHIBITION · DELHI
          </motion.div>

          <h1 className="glitch font-display text-6xl font-black tracking-[0.22em] text-verde-green sm:text-8xl">
            <motion.span
              animate={{
                textShadow: [
                  "0 0 25px rgba(34,197,94,0.5)",
                  "0 0 60px rgba(34,197,94,1)",
                  "0 0 25px rgba(34,197,94,0.5)",
                ],
              }}
              transition={{ duration: 2.5, repeat: Infinity }}
            >
              VERDE
            </motion.span>
          </h1>

          <motion.p
            initial={{ opacity: 0, letterSpacing: "0.2em" }}
            animate={{ opacity: 1, letterSpacing: "0.5em" }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="mt-4 text-xs text-verde-text sm:text-sm"
          >
            AUTONOMOUS PLANT OS · V3.0
          </motion.p>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mx-auto mt-5 max-w-lg text-[11px] leading-relaxed text-verde-muted"
          >
            Industrial-grade smart garden: remote irrigation, live telemetry,
            weather-aware watering, and AI-powered leaf disease diagnostics —
            from anywhere on Earth.
          </motion.p>
        </motion.div>

        {/* Feature chips */}
        <div className="mt-12 grid grid-cols-2 gap-3 md:grid-cols-4">
          {FEATURES.map((f, i) => {
            const Icon = f.icon;
            return (
              <motion.div
                key={f.label}
                initial={{ opacity: 0, y: 24, scale: 0.92 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{
                  delay: 0.5 + i * 0.12,
                  type: "spring",
                  stiffness: 120,
                  damping: 16,
                }}
                whileHover={{ y: -6, transition: { duration: 0.2 } }}
                className="crt sheen relative rounded-xl border border-verde-border bg-verde-panel/70 p-4 backdrop-blur transition-all duration-300 hover:border-verde-green/50 hover:shadow-glow"
              >
                <motion.div
                  animate={{ y: [0, -3, 0] }}
                  transition={{ duration: 2.2, repeat: Infinity, delay: i * 0.35 }}
                >
                  <Icon size={17} className="mx-auto mb-2 text-verde-green" />
                </motion.div>
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
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.05 }}
          className="mt-12"
        >
          <Link
            href="/dashboard"
            className="group relative inline-flex items-center gap-2 overflow-hidden rounded-lg border border-verde-green bg-verde-green/10 px-9 py-4 text-sm tracking-[0.25em] text-verde-green transition-all duration-300 hover:bg-verde-green/20 hover:shadow-glow-lg"
          >
            {/* animated sweep inside the button */}
            <motion.span
              className="pointer-events-none absolute inset-y-0 w-1/3"
              style={{
                background:
                  "linear-gradient(100deg, transparent, rgba(34,197,94,0.25), transparent)",
              }}
              animate={{ left: ["-40%", "120%"] }}
              transition={{ duration: 2.2, repeat: Infinity, ease: "easeInOut" }}
            />
            ENTER CONTROL DECK
            <ChevronRight
              size={16}
              className="transition-transform duration-300 group-hover:translate-x-1.5"
            />
          </Link>
          <p className="mt-7 text-[8px] tracking-[0.3em] text-verde-muted">
            BUILT BY AARAV & ANUJ · ESP32 WROOM-32 + ESP32-CAM · FIREBASE RTDB
          </p>
        </motion.div>
      </div>
    </main>
  );
}
