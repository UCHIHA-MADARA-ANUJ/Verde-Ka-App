"use client";
// ============================================================
// VERDE BOOT SEQUENCE — cinematic loader:
// growing plant SVG (draw-on animation), orbiting particles,
// radar rings, typed kernel log, glitch title, progress core.
// Holds until the Firebase session settles, then zoom-dissolves.
// ============================================================
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const BOOT_LINES = [
  "verde-kernel 3.0.0 booting…",
  "sensor bus……… DHT22 · HC-SR04 · LDR · SOIL-GATED",
  "actuators……… PUMP_RELAY(25) · UV_LED(26)",
  "vision node…… ESP32-CAM · OV2640 · 8MHz XCLK",
  "cloud bridge… FIREBASE RTDB · WEBSOCKET",
  "ai stack……… CROP.HEALTH + GEMINI 2.5 FLASH",
  "auth………… ANONYMOUS JWT SESSION",
  "ALL SYSTEMS NOMINAL",
];

// Deterministic pseudo-random (avoids SSR hydration mismatch)
function prand(i, salt) {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export default function BootLoader({ done }) {
  const [lineCount, setLineCount] = useState(0);
  const [progress, setProgress] = useState(0);
  const [exit, setExit] = useState(false);

  useEffect(() => {
    const timers = BOOT_LINES.map((_, i) =>
      setTimeout(() => setLineCount(i + 1), 260 * i + 200)
    );
    const prog = setInterval(() => {
      setProgress((p) => {
        const target = done ? 100 : 90;
        const step = done ? 6 : Math.random() * 5 + 1.5;
        return Math.min(p + step, target);
      });
    }, 80);
    return () => {
      timers.forEach(clearTimeout);
      clearInterval(prog);
    };
  }, [done]);

  useEffect(() => {
    if (done && progress >= 100) {
      const t = setTimeout(() => setExit(true), 420);
      return () => clearTimeout(t);
    }
  }, [done, progress]);

  return (
    <AnimatePresence>
      {!exit && (
        <motion.div
          exit={{ opacity: 0, scale: 1.06, filter: "blur(6px)" }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="fixed inset-0 z-[100] flex items-center justify-center overflow-hidden bg-verde-bg"
        >
          {/* Ambient radial glow */}
          <div
            className="pointer-events-none absolute inset-0"
            style={{
              background:
                "radial-gradient(ellipse 60% 50% at 50% 45%, rgba(34,197,94,0.08), transparent 70%)",
            }}
          />

          {/* Orbiting particles */}
          {Array.from({ length: 14 }).map((_, i) => {
            const angle = (i / 14) * Math.PI * 2;
            const radius = 190 + prand(i, 1) * 130;
            return (
              <motion.span
                key={i}
                className="pointer-events-none absolute left-1/2 top-1/2 h-1 w-1 rounded-full bg-verde-green"
                style={{ boxShadow: "0 0 6px rgba(34,197,94,0.9)" }}
                animate={{
                  x: [
                    Math.cos(angle) * radius,
                    Math.cos(angle + Math.PI) * radius,
                    Math.cos(angle + Math.PI * 2) * radius,
                  ],
                  y: [
                    Math.sin(angle) * radius * 0.55,
                    Math.sin(angle + Math.PI) * radius * 0.55,
                    Math.sin(angle + Math.PI * 2) * radius * 0.55,
                  ],
                  opacity: [0.15, 0.9, 0.15],
                  scale: [0.6, 1.4, 0.6],
                }}
                transition={{
                  duration: 9 + prand(i, 2) * 6,
                  repeat: Infinity,
                  ease: "linear",
                }}
              />
            );
          })}

          {/* Radar rings */}
          {[300, 480, 660].map((size, i) => (
            <motion.div
              key={size}
              className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full border border-verde-green/15"
              style={{ width: size, height: size }}
              animate={{ scale: [1, 1.05, 1], opacity: [0.5, 0.15, 0.5] }}
              transition={{ duration: 3.2, delay: i * 0.55, repeat: Infinity }}
            />
          ))}

          <div className="relative z-10 w-full max-w-xl px-6">
            {/* Growing plant emblem */}
            <div className="mx-auto mb-5 h-28 w-28">
              <svg viewBox="0 0 100 100" className="h-full w-full">
                {/* stem */}
                <motion.path
                  d="M50 92 C50 70 50 55 50 38"
                  fill="none"
                  stroke="#22c55e"
                  strokeWidth="3"
                  strokeLinecap="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 1.1, ease: "easeOut" }}
                  style={{ filter: "drop-shadow(0 0 5px rgba(34,197,94,0.8))" }}
                />
                {/* left leaf */}
                <motion.path
                  d="M50 64 C38 62 28 52 27 40 C40 42 49 51 50 64 Z"
                  fill="rgba(34,197,94,0.25)"
                  stroke="#22c55e"
                  strokeWidth="2"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 0.9, delay: 0.7, ease: "easeOut" }}
                  style={{ filter: "drop-shadow(0 0 5px rgba(34,197,94,0.7))" }}
                />
                {/* right leaf */}
                <motion.path
                  d="M50 52 C62 50 72 40 73 28 C60 30 51 39 50 52 Z"
                  fill="rgba(34,197,94,0.25)"
                  stroke="#22c55e"
                  strokeWidth="2"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 0.9, delay: 1.0, ease: "easeOut" }}
                  style={{ filter: "drop-shadow(0 0 5px rgba(34,197,94,0.7))" }}
                />
                {/* bud */}
                <motion.circle
                  cx="50"
                  cy="34"
                  r="5"
                  fill="#22c55e"
                  initial={{ scale: 0 }}
                  animate={{ scale: [0, 1.35, 1] }}
                  transition={{ duration: 0.6, delay: 1.5 }}
                  style={{ filter: "drop-shadow(0 0 10px rgba(34,197,94,1))" }}
                />
                {/* soil line */}
                <motion.path
                  d="M28 92 L72 92"
                  stroke="#15803d"
                  strokeWidth="3"
                  strokeLinecap="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.5 }}
                />
              </svg>
            </div>

            {/* Glitch title */}
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8 text-center"
            >
              <motion.h1
                className="glitch font-display text-4xl font-black tracking-[0.35em] text-verde-green sm:text-5xl"
                animate={{
                  textShadow: [
                    "0 0 18px rgba(34,197,94,0.5)",
                    "0 0 42px rgba(34,197,94,0.95)",
                    "0 0 18px rgba(34,197,94,0.5)",
                  ],
                }}
                transition={{ duration: 2.2, repeat: Infinity }}
              >
                VERDE
              </motion.h1>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="mt-2 text-[9px] tracking-[0.6em] text-verde-muted"
              >
                AUTONOMOUS · PLANT · OS
              </motion.p>
            </motion.div>

            {/* Kernel log */}
            <div className="crt relative mb-6 h-44 overflow-hidden rounded-lg border border-verde-border bg-verde-panel/90 p-4 backdrop-blur">
              {BOOT_LINES.slice(0, lineCount).map((line, i) => (
                <motion.p
                  key={line}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.25 }}
                  className={`mb-1 text-[10px] leading-relaxed sm:text-[11px] ${
                    i === BOOT_LINES.length - 1
                      ? "text-verde-green text-glow-strong"
                      : "text-verde-dim"
                  }`}
                >
                  <motion.span
                    className="mr-2 inline-block text-verde-green"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 500, damping: 20 }}
                  >
                    ▸
                  </motion.span>
                  {line}
                </motion.p>
              ))}
              <span className="animate-blink text-verde-green">▌</span>
            </div>

            {/* Progress core */}
            <div className="relative h-2 w-full overflow-hidden rounded-full bg-verde-border/60">
              <motion.div
                className="relative h-full rounded-full"
                style={{
                  background:
                    "linear-gradient(90deg, #15803d, #22c55e, #4ade80)",
                  boxShadow: "0 0 16px rgba(34,197,94,0.9)",
                }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: "easeOut", duration: 0.25 }}
              >
                <div
                  className="absolute inset-0 opacity-60"
                  style={{
                    background:
                      "repeating-linear-gradient(45deg, transparent, transparent 6px, rgba(255,255,255,0.15) 6px, rgba(255,255,255,0.15) 12px)",
                  }}
                />
              </motion.div>
            </div>
            <div className="mt-2 flex justify-between text-[9px] text-verde-muted">
              <motion.span
                animate={{ opacity: [1, 0.4, 1] }}
                transition={{ duration: 1.6, repeat: Infinity }}
              >
                {done ? "UPLINK SECURED — ENTERING DECK" : "ESTABLISHING SECURE UPLINK…"}
              </motion.span>
              <span className="font-display text-verde-green text-glow">
                {Math.floor(progress)}%
              </span>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
