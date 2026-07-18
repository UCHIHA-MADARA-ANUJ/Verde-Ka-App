"use client";
// Radial moisture gauge — spring-animated arc, tick ring, threshold
// marker, orbiting spark, animated number core. Pure SVG, real data.
import { motion, useSpring, useTransform, useMotionValue } from "framer-motion";
import { useEffect } from "react";
import AnimatedNumber from "@/components/AnimatedNumber";

const R = 62;
const CIRC = 2 * Math.PI * R;

export default function MoistureGauge({ value = 0, threshold = 40 }) {
  const pct = Math.max(0, Math.min(100, value));
  const dry = pct < threshold;

  const mv = useMotionValue(0);
  const spring = useSpring(mv, { stiffness: 60, damping: 18 });
  const dashOffset = useTransform(spring, (v) => CIRC - (v / 100) * CIRC);

  useEffect(() => {
    mv.set(pct);
  }, [pct, mv]);

  // Threshold marker position
  const thetaT = (threshold / 100) * Math.PI * 2 - Math.PI / 2;
  const tx = 80 + Math.cos(thetaT) * R;
  const ty = 80 + Math.sin(thetaT) * R;

  const color = dry ? "#f59e0b" : "#22c55e";

  return (
    <div className="crt sheen border-breathe relative flex flex-col items-center rounded-xl border bg-verde-card p-5 transition-all duration-300 hover:shadow-glow-lg">
      <p className="mb-3 self-start text-[10px] tracking-widest text-verde-muted">
        ▓ SOIL MOISTURE
      </p>
      <div className="relative h-44 w-44">
        <svg viewBox="0 0 160 160" className="h-full w-full -rotate-90">
          {/* tick ring */}
          {Array.from({ length: 40 }).map((_, i) => {
            const a = (i / 40) * Math.PI * 2;
            const inner = 73;
            const outer = i % 5 === 0 ? 78 : 76;
            return (
              <line
                key={i}
                x1={80 + Math.cos(a) * inner}
                y1={80 + Math.sin(a) * inner}
                x2={80 + Math.cos(a) * outer}
                y2={80 + Math.sin(a) * outer}
                stroke={
                  (i / 40) * 100 <= pct ? color : "rgba(31,42,31,0.9)"
                }
                strokeWidth={i % 5 === 0 ? 2 : 1}
              />
            );
          })}
          {/* track */}
          <circle
            cx="80" cy="80" r={R}
            fill="none" stroke="#1f2a1f" strokeWidth="9"
          />
          {/* progress arc (spring-driven) */}
          <motion.circle
            cx="80" cy="80" r={R}
            fill="none"
            stroke={color}
            strokeWidth="9"
            strokeLinecap="round"
            strokeDasharray={CIRC}
            style={{
              strokeDashoffset: dashOffset,
              filter: `drop-shadow(0 0 7px ${color}cc)`,
            }}
          />
          {/* threshold marker */}
          <circle
            cx={tx} cy={ty} r="4"
            fill="#0c0c0c"
            stroke="#f59e0b"
            strokeWidth="2"
            style={{ filter: "drop-shadow(0 0 4px rgba(245,158,11,0.9))" }}
          />
        </svg>

        {/* rotating spark on the arc tip */}
        <motion.div
          className="pointer-events-none absolute inset-0"
          animate={{ rotate: (pct / 100) * 360 }}
          transition={{ type: "spring", stiffness: 60, damping: 18 }}
        >
          <span
            className="absolute left-1/2 top-[7px] h-2 w-2 -translate-x-1/2 rounded-full"
            style={{
              background: color,
              boxShadow: `0 0 12px 3px ${color}`,
            }}
          />
        </motion.div>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <p
            className={`font-display text-4xl font-bold text-glow-strong ${
              dry ? "text-amber-400" : "text-verde-green"
            }`}
          >
            <AnimatedNumber value={pct} />
            <span className="text-lg">%</span>
          </p>
          <span className="mt-1 text-[9px] tracking-widest text-verde-muted">
            TARGET {threshold}%
          </span>
        </div>
      </div>

      <motion.p
        key={dry ? "dry" : "ok"}
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        className={`mt-2 flex items-center gap-2 text-[10px] ${
          dry ? "text-amber-400" : "text-verde-dim"
        }`}
      >
        <span
          className={`ping-dot relative inline-block h-1.5 w-1.5 rounded-full ${
            dry ? "bg-amber-400" : "bg-verde-green"
          }`}
        />
        {dry ? "BELOW TARGET — IRRIGATION QUEUED" : "WITHIN TARGET RANGE"}
      </motion.p>
    </div>
  );
}
