"use client";
// ============================================================
// BOOT LOADER — cinematic full-screen boot sequence shown while
// the Firebase session initializes. Typed boot lines + progress
// bar + radar sweep. Minimum display ~2.2s for the full effect.
// ============================================================
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const BOOT_LINES = [
  { t: "VERDE PLANT OS v3.0 — KERNEL INIT", d: 0 },
  { t: "mounting sensor bus........... DHT22 · HC-SR04 · LDR · SOIL", d: 250 },
  { t: "actuator rail check........... PUMP_RELAY(25) · UV_LED(26)", d: 500 },
  { t: "vision node handshake......... ESP32-CAM @ 8MHz XCLK", d: 750 },
  { t: "opening cloud bridge.......... FIREBASE RTDB WEBSOCKET", d: 1000 },
  { t: "ai stack...................... PLANT.ID + GEMINI 2.0 FLASH", d: 1250 },
  { t: "authenticating session........ ANONYMOUS JWT", d: 1500 },
  { t: "SYSTEM NOMINAL — LAUNCHING CONTROL DECK", d: 1850 },
];

export default function BootLoader({ done }) {
  const [visibleLines, setVisibleLines] = useState(0);
  const [progress, setProgress] = useState(0);
  const [exit, setExit] = useState(false);

  useEffect(() => {
    const timers = BOOT_LINES.map((line, i) =>
      setTimeout(() => setVisibleLines(i + 1), line.d)
    );
    const prog = setInterval(() => {
      setProgress((p) => Math.min(p + Math.random() * 7 + 2, done ? 100 : 92));
    }, 90);
    return () => {
      timers.forEach(clearTimeout);
      clearInterval(prog);
    };
  }, [done]);

  useEffect(() => {
    if (done && progress >= 100) {
      const t = setTimeout(() => setExit(true), 350);
      return () => clearTimeout(t);
    }
  }, [done, progress]);

  return (
    <AnimatePresence>
      {!exit && (
        <motion.div
          exit={{ opacity: 0, scale: 1.04 }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-verde-bg"
        >
          {/* Radar rings */}
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center opacity-20">
            {[280, 480, 680].map((size, i) => (
              <motion.div
                key={size}
                className="absolute rounded-full border border-verde-green/40"
                style={{ width: size, height: size }}
                animate={{ scale: [1, 1.06, 1], opacity: [0.4, 0.15, 0.4] }}
                transition={{ duration: 3, delay: i * 0.5, repeat: Infinity }}
              />
            ))}
          </div>

          <div className="relative w-full max-w-xl px-6">
            {/* Logo */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8 text-center"
            >
              <motion.div
                animate={{
                  textShadow: [
                    "0 0 20px rgba(34,197,94,0.6)",
                    "0 0 45px rgba(34,197,94,0.9)",
                    "0 0 20px rgba(34,197,94,0.6)",
                  ],
                }}
                transition={{ duration: 2, repeat: Infinity }}
                className="text-5xl tracking-[0.3em] text-verde-green"
              >
                VERDE
              </motion.div>
              <p className="mt-2 text-[10px] tracking-[0.5em] text-verde-muted">
                AUTONOMOUS PLANT OS · V3.0
              </p>
            </motion.div>

            {/* Boot lines */}
            <div className="crt relative mb-6 h-48 overflow-hidden rounded-lg border border-verde-border bg-verde-panel p-4">
              {BOOT_LINES.slice(0, visibleLines).map((line, i) => (
                <motion.p
                  key={line.t}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  className={`mb-1 text-[10px] leading-relaxed sm:text-[11px] ${
                    i === BOOT_LINES.length - 1
                      ? "text-verde-green text-glow"
                      : "text-verde-dim"
                  }`}
                >
                  <span className="mr-2 text-verde-green">[ OK ]</span>
                  {line.t}
                </motion.p>
              ))}
              <span className="animate-blink text-verde-green">▌</span>
            </div>

            {/* Progress bar */}
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-verde-border">
              <motion.div
                className="h-full rounded-full bg-verde-green"
                style={{ boxShadow: "0 0 12px rgba(34,197,94,0.8)" }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: "easeOut" }}
              />
            </div>
            <div className="mt-2 flex justify-between text-[9px] text-verde-muted">
              <span>INITIALIZING SECURE UPLINK…</span>
              <span className="text-verde-green">{Math.floor(progress)}%</span>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
