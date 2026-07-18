"use client";
// Radial glowing ring gauge for soil moisture % (SVG, zero deps).
import { motion } from "framer-motion";

export default function MoistureGauge({ value = 0, threshold = 40 }) {
  const R = 64;
  const CIRC = 2 * Math.PI * R;
  const pct = Math.max(0, Math.min(100, value));
  const dash = (pct / 100) * CIRC;
  const dry = pct < threshold;

  return (
    <div className="crt relative flex flex-col items-center rounded-lg border border-verde-border bg-verde-card p-5 transition-shadow hover:shadow-glow">
      <p className="mb-3 self-start text-[10px] tracking-widest text-verde-muted">
        ▓ SOIL MOISTURE
      </p>
      <div className="relative h-40 w-40">
        <svg viewBox="0 0 160 160" className="h-full w-full -rotate-90">
          <circle
            cx="80" cy="80" r={R}
            fill="none" stroke="#1f2a1f" strokeWidth="10"
          />
          <motion.circle
            cx="80" cy="80" r={R}
            fill="none"
            stroke={dry ? "#f59e0b" : "#22c55e"}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${CIRC}`}
            initial={{ strokeDasharray: `0 ${CIRC}` }}
            animate={{ strokeDasharray: `${dash} ${CIRC}` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            style={{
              filter: `drop-shadow(0 0 6px ${
                dry ? "rgba(245,158,11,0.7)" : "rgba(34,197,94,0.7)"
              })`,
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className={`text-3xl text-glow ${
              dry ? "text-amber-400" : "text-verde-green"
            }`}
          >
            {pct}%
          </span>
          <span className="text-[9px] text-verde-muted">
            TARGET {threshold}%
          </span>
        </div>
      </div>
      <p
        className={`mt-2 text-[10px] ${
          dry ? "text-amber-400" : "text-verde-dim"
        }`}
      >
        {dry ? "● BELOW TARGET — IRRIGATION QUEUED" : "● WITHIN TARGET RANGE"}
      </p>
    </div>
  );
}
