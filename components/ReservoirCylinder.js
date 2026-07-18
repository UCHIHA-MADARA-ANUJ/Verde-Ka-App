"use client";
// Blue-gradient liquid cylinder for the bucket reservoir.
// Below 10% → flashing red CRITICAL card (dry-run prevention, doc 13).
import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

export default function ReservoirCylinder({ value = 0 }) {
  const pct = Math.max(0, Math.min(100, value));
  const critical = pct < 10;

  return (
    <div
      className={`crt relative flex flex-col rounded-lg border p-5 transition-shadow ${
        critical
          ? "border-verde-danger bg-red-950/20 animate-pulse-red"
          : "border-verde-border bg-verde-card hover:shadow-glow-water"
      }`}
    >
      <p className="mb-3 text-[10px] tracking-widest text-verde-muted">
        ▓ WATER RESERVOIR
      </p>

      <div className="flex items-end gap-4">
        {/* Cylinder */}
        <div className="relative h-36 w-16 overflow-hidden rounded-b-xl rounded-t-md border border-verde-border bg-verde-panel">
          <motion.div
            className="absolute bottom-0 left-0 right-0"
            initial={{ height: 0 }}
            animate={{ height: `${pct}%` }}
            transition={{ duration: 0.9, ease: "easeOut" }}
            style={{
              background: critical
                ? "linear-gradient(180deg,#ef4444,#7f1d1d)"
                : "linear-gradient(180deg,#38bdf8,#0369a1)",
              boxShadow: critical
                ? "0 0 14px rgba(239,68,68,0.6)"
                : "0 0 14px rgba(56,189,248,0.5)",
            }}
          >
            <div className="h-1 w-full bg-white/30" />
          </motion.div>
          {/* Graduations */}
          {[25, 50, 75].map((g) => (
            <div
              key={g}
              className="absolute left-0 h-px w-2 bg-verde-border"
              style={{ bottom: `${g}%` }}
            />
          ))}
        </div>

        <div className="flex-1">
          <p
            className={`text-3xl text-glow ${
              critical ? "text-verde-danger" : "text-verde-water"
            }`}
          >
            {pct}%
          </p>
          {critical ? (
            <p className="mt-2 flex items-start gap-1 text-[10px] leading-snug text-verde-danger">
              <AlertTriangle size={12} className="mt-0.5 shrink-0" />
              CRITICAL: Reservoir empty! Pump de-activated to prevent motor
              burnout. Refill bucket manually.
            </p>
          ) : (
            <p className="mt-2 text-[10px] text-verde-dim">
              ● HC-SR04 SONAR LEVEL NOMINAL
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
