"use client";
// Glowing green Recharts AreaChart of moisture history (24h window).
// Lazy-loaded from the dashboard to keep first paint fast (doc 16).
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

function VerdeTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded border border-verde-green/40 bg-verde-panel px-3 py-2 text-[11px] shadow-glow-sm">
      <p className="text-verde-muted">{label}</p>
      <p className="text-verde-green">MOISTURE: {payload[0].value}%</p>
    </div>
  );
}

export default function MoistureChart({ points, threshold }) {
  return (
    <div className="crt relative flex h-full min-h-[280px] flex-col rounded-lg border border-verde-border bg-verde-card p-5 transition-shadow hover:shadow-glow">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-[10px] tracking-widest text-verde-muted">
          ▓ MOISTURE HISTORY · LAST 24H
        </p>
        <p className="text-[10px] text-verde-dim">
          {points.length} SAMPLES
        </p>
      </div>

      {points.length === 0 ? (
        <div className="flex flex-1 items-center justify-center text-[11px] text-verde-muted">
          ── AWAITING FIRST TELEMETRY SAMPLES ──
        </div>
      ) : (
        <div className="h-56 w-full flex-1">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={points} margin={{ top: 4, right: 8, left: -22, bottom: 0 }}>
              <defs>
                <linearGradient id="verdeFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#22c55e" stopOpacity={0.45} />
                  <stop offset="100%" stopColor="#22c55e" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="#1f2a1f" strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tick={{ fill: "#6b7280", fontSize: 9, fontFamily: "inherit" }}
                stroke="#1f2a1f"
                minTickGap={40}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fill: "#6b7280", fontSize: 9, fontFamily: "inherit" }}
                stroke="#1f2a1f"
              />
              <Tooltip content={<VerdeTooltip />} />
              <ReferenceLine
                y={threshold}
                stroke="#f59e0b"
                strokeDasharray="4 4"
                label={{
                  value: `TARGET ${threshold}%`,
                  fill: "#f59e0b",
                  fontSize: 9,
                  position: "insideTopRight",
                }}
              />
              <Area
                type="monotone"
                dataKey="moisture"
                stroke="#22c55e"
                strokeWidth={2}
                fill="url(#verdeFill)"
                isAnimationActive={true}
                animationDuration={600}
                style={{ filter: "drop-shadow(0 0 4px rgba(34,197,94,0.6))" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
