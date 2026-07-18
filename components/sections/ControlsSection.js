"use client";
// ═══ SECTION: CONTROLS — the full override deck, expanded ═══
import { motion } from "framer-motion";
import ControlDeck from "@/components/ControlDeck";
import WeatherBadge from "@/components/WeatherBadge";
import { ShieldCheck, Zap, CloudRain, Timer } from "lucide-react";

const RULES = [
  {
    icon: Zap,
    title: "AUTONOMOUS IRRIGATION",
    body: "In AUTO mode the ESP32 waters whenever soil moisture drops below your target — even if this dashboard is closed or Wi-Fi is dead.",
  },
  {
    icon: ShieldCheck,
    title: "DRY-RUN PROTECTION",
    body: "Pump is hard-blocked whenever the reservoir is under 10%, protecting the motor from burning out. Refill the bucket to unlock.",
  },
  {
    icon: CloudRain,
    title: "WEATHER HOLD",
    body: "An hourly cloud job checks Delhi weather. If rain is predicted, irrigation suspends automatically to save water.",
  },
  {
    icon: Timer,
    title: "SUB-100MS SYNC",
    body: "Every toggle streams over a live WebSocket to the ESP32. Physical relays fire in under a tenth of a second.",
  },
];

export default function ControlsSection({
  controls,
  setControl,
  online,
  sensors,
  sessionReady,
}) {
  return (
    <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
      <div className="space-y-4">
        <WeatherBadge
          enabled={sessionReady}
          weatherOverride={controls.weather_override}
        />
        <ControlDeck
          controls={controls}
          setControl={setControl}
          online={online}
          tankLevel={sensors.tank_level}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
        {RULES.map((r, i) => {
          const Icon = r.icon;
          return (
            <motion.div
              key={r.title}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className="crt relative rounded-lg border border-verde-border bg-verde-card p-4 transition-all duration-200 hover:shadow-glow"
            >
              <div className="mb-2 flex items-center gap-2 text-verde-green">
                <Icon size={14} />
                <p className="text-[10px] tracking-widest">{r.title}</p>
              </div>
              <p className="text-[10px] leading-relaxed text-verde-dim">
                {r.body}
              </p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
