"use client";
// ═══ SECTION: SYSTEM — architecture, node health & stack info ═══
import { motion } from "framer-motion";
import {
  Cpu,
  Camera,
  Database,
  Globe,
  Wifi,
  WifiOff,
  GitBranch,
} from "lucide-react";

function NodeCard({ i, icon: Icon, title, status, ok, lines }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: i * 0.08 }}
      className="crt relative rounded-lg border border-verde-border bg-verde-card p-5 transition-all duration-200 hover:shadow-glow"
    >
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2 text-verde-text">
          <Icon size={15} className="text-verde-green" />
          <p className="text-[11px] tracking-widest">{title}</p>
        </div>
        <span
          className={`flex items-center gap-1.5 rounded border px-2 py-0.5 text-[8px] tracking-wider ${
            ok
              ? "border-verde-green/50 text-verde-green"
              : "border-verde-danger/60 text-verde-danger animate-pulse"
          }`}
        >
          {ok ? <Wifi size={9} /> : <WifiOff size={9} />}
          {status}
        </span>
      </div>
      <div className="space-y-1">
        {lines.map((l) => (
          <p key={l} className="text-[9px] leading-relaxed text-verde-dim">
            · {l}
          </p>
        ))}
      </div>
    </motion.div>
  );
}

export default function SystemSection({ online, sensors, controls }) {
  const lastWrite = sensors.last_updated
    ? new Date(
        sensors.last_updated < 1e12
          ? sensors.last_updated * 1000
          : sensors.last_updated
      ).toLocaleString()
    : "never";

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <NodeCard
          i={0}
          icon={Cpu}
          title="MAIN BRAIN · ESP32 WROOM-32"
          status={online ? "ONLINE" : "OFFLINE"}
          ok={online}
          lines={[
            "Xtensa dual-core LX6 @ 240MHz · 520KB SRAM",
            "Techtonics 30-pin G-V-S breakout shield (5V jumper)",
            "Telemetry every 4s over Firebase WebSocket",
            `Last telemetry write: ${lastWrite}`,
            "Autonomous watering continues even if cloud is down",
          ]}
        />
        <NodeCard
          i={1}
          icon={Camera}
          title="VISION NODE · ESP32-CAM"
          status={controls.capture_photo ? "CAPTURING" : "IDLE / POLLING"}
          ok={true}
          lines={[
            "AI-Thinker · OV2640 2MP · 4MB PSRAM",
            "XCLK throttled to 8MHz (kills RF antenna interference)",
            "Polls capture flag every 2s · low-power idle",
            "POSTs raw JPEG to Vercel /api/upload-photo",
            "MB USB shield · fully wireless from main deck",
          ]}
        />
        <NodeCard
          i={2}
          icon={Database}
          title="CLOUD SYNC · FIREBASE RTDB"
          status="CONNECTED"
          ok={true}
          lines={[
            "WebSocket JSON tree sync · <100ms round trip",
            "Nodes: /sensors /controls /historical_logs /latest_scan /weather",
            "Rules locked to authenticated sessions (auth != null)",
            "Anonymous JWT session for instant judge access",
          ]}
        />
        <NodeCard
          i={3}
          icon={Globe}
          title="SERVERLESS · VERCEL EDGE"
          status="DEPLOYED"
          ok={true}
          lines={[
            "/api/upload-photo — Node runtime, x-api-key guarded",
            "/api/analyze-plant — Edge, Plant.id → Gemini 2.0 Flash",
            "/api/weather-sync — hourly Delhi OpenWeatherMap cron",
            "/api/cleanup-storage — nightly 15-day TTL sweep",
          ]}
        />
      </div>

      {/* Architecture diagram */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35 }}
        className="crt relative overflow-x-auto rounded-lg border border-verde-border bg-verde-card p-5"
      >
        <p className="mb-4 text-[9px] tracking-widest text-verde-muted">
          ▓ SYSTEM TOPOLOGY
        </p>
        <pre className="min-w-[560px] text-[9px] leading-relaxed text-verde-dim">
{`  [ESP32 MAIN BRAIN]────4s telemetry────►┐
     sensors · pump · UV LED             │
                                         ▼
                              ┌─────────────────────┐
  [ESP32-CAM]──poll 2s───────►│   FIREBASE RTDB     │◄──WebSocket──[THIS DASHBOARD]
     snap on demand           │  the state machine  │                (Vercel)
        │                     └─────────────────────┘                    │
        │                                ▲                               │
        └────POST JPEG────► [/api/upload-photo] ── resets flag           │
                                     │                                   │
                          [Plant.id → Gemini 2.0 Flash] ◄────────────────┘
                                 AI diagnosis                    [/api/weather-sync]
                                                                  hourly Delhi cron`}
        </pre>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.45 }}
        className="flex flex-wrap items-center gap-3 rounded-lg border border-verde-border bg-verde-panel px-4 py-3 text-[9px] text-verde-muted"
      >
        <GitBranch size={11} className="text-verde-green" />
        <span>NEXT.JS 14 · TAILWIND · FRAMER MOTION · RECHARTS · FIREBASE · VERCEL</span>
        <span className="ml-auto">BUILT BY AARAV & ANUJ · PROJECT VERDE V3.0</span>
      </motion.div>
    </div>
  );
}
