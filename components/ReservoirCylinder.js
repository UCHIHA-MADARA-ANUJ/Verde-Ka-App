"use client";
// Reservoir tank — animated liquid with dual moving wave surfaces,
// rising bubbles, graduation marks, critical flash-red state.
import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";
import AnimatedNumber from "@/components/AnimatedNumber";

const BUBBLES = [
  { l: "20%", d: "2.6s", delay: "0s", bx: "6px", s: 3 },
  { l: "45%", d: "3.4s", delay: "0.8s", bx: "-5px", s: 2 },
  { l: "65%", d: "2.9s", delay: "1.6s", bx: "4px", s: 4 },
  { l: "80%", d: "3.8s", delay: "0.4s", bx: "-6px", s: 2 },
  { l: "33%", d: "3.1s", delay: "2.1s", bx: "5px", s: 3 },
];

export default function ReservoirCylinder({ value = 0 }) {
  const pct = Math.max(0, Math.min(100, value));
  const critical = pct < 10;
  const liquidTop = `${100 - pct}%`;

  const mainColor = critical ? "#ef4444" : "#38bdf8";
  const deepColor = critical ? "#7f1d1d" : "#075985";

  return (
    <div
      className={`crt sheen relative flex flex-col rounded-xl border p-5 transition-all duration-300 ${
        critical
          ? "border-verde-danger bg-red-950/20 animate-pulse-red"
          : "border-verde-border bg-verde-card hover:shadow-glow-water"
      }`}
    >
      <p className="mb-3 text-[10px] tracking-widest text-verde-muted">
        ▓ WATER RESERVOIR
      </p>

      <div className="flex items-end gap-5">
        {/* Tank */}
        <div className="relative h-44 w-24 overflow-hidden rounded-b-2xl rounded-t-lg border border-verde-border bg-verde-panel/80">
          {/* Liquid body */}
          <motion.div
            className="absolute bottom-0 left-0 right-0 overflow-hidden"
            initial={{ height: 0 }}
            animate={{ height: `${pct}%` }}
            transition={{ type: "spring", stiffness: 45, damping: 16 }}
            style={{
              background: `linear-gradient(180deg, ${mainColor}dd 0%, ${deepColor} 100%)`,
              boxShadow: `0 0 18px ${mainColor}66`,
            }}
          >
            {/* Bubbles inside liquid */}
            {!critical &&
              BUBBLES.map((b, i) => (
                <span
                  key={i}
                  className="bubble absolute bottom-1 rounded-full bg-white/40"
                  style={{
                    left: b.l,
                    width: b.s,
                    height: b.s,
                    "--bd": b.d,
                    "--bdelay": b.delay,
                    "--bx": b.bx,
                  }}
                />
              ))}
          </motion.div>

          {/* Wave surface — two layers sliding at the liquid line */}
          <motion.div
            className="pointer-events-none absolute left-0 right-0"
            initial={false}
            animate={{ top: liquidTop }}
            transition={{ type: "spring", stiffness: 45, damping: 16 }}
            style={{ height: 12, marginTop: -6 }}
          >
            <div className="wave absolute h-full w-[200%]">
              <svg viewBox="0 0 200 12" preserveAspectRatio="none" className="h-full w-full">
                <path
                  d="M0 6 Q12.5 0 25 6 T50 6 T75 6 T100 6 T125 6 T150 6 T175 6 T200 6 V12 H0 Z"
                  fill={mainColor}
                  opacity="0.9"
                />
              </svg>
            </div>
            <div className="wave2 absolute h-full w-[200%]">
              <svg viewBox="0 0 200 12" preserveAspectRatio="none" className="h-full w-full">
                <path
                  d="M0 7 Q12.5 2 25 7 T50 7 T75 7 T100 7 T125 7 T150 7 T175 7 T200 7 V12 H0 Z"
                  fill="#ffffff"
                  opacity="0.25"
                />
              </svg>
            </div>
          </motion.div>

          {/* Glass shine */}
          <div className="pointer-events-none absolute inset-y-0 left-1 w-2 rounded-full bg-white/5" />

          {/* Graduations */}
          {[25, 50, 75].map((g) => (
            <div key={g} className="absolute left-0 flex items-center gap-1" style={{ bottom: `${g}%` }}>
              <div className="h-px w-2.5 bg-verde-border" />
              <span className="text-[6px] text-verde-muted">{g}</span>
            </div>
          ))}
        </div>

        <div className="flex-1">
          <p
            className={`font-display text-4xl font-bold text-glow-strong ${
              critical ? "text-verde-danger" : "text-verde-water"
            }`}
          >
            <AnimatedNumber value={pct} />
            <span className="text-lg">%</span>
          </p>
          {critical ? (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-2 flex items-start gap-1.5 text-[10px] leading-snug text-verde-danger"
            >
              <AlertTriangle size={13} className="mt-0.5 shrink-0" />
              CRITICAL: Reservoir empty! Pump de-activated to prevent motor
              burnout. Refill bucket manually.
            </motion.p>
          ) : (
            <p className="mt-2 flex items-center gap-2 text-[10px] text-verde-dim">
              <span className="ping-dot relative inline-block h-1.5 w-1.5 rounded-full bg-verde-water" />
              HC-SR04 SONAR · LEVEL NOMINAL
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
