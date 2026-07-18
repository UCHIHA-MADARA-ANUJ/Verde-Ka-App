"use client";
// ═══ SECTION: OVERVIEW — mission-control snapshot of everything ═══
import { motion } from "framer-motion";
import {
  Droplet,
  Thermometer,
  Waves,
  SunMedium,
  Lightbulb,
  Camera,
  CloudRain,
  Bot,
  Hand,
} from "lucide-react";
import MoistureGauge from "@/components/MoistureGauge";
import ReservoirCylinder from "@/components/ReservoirCylinder";
import AnimatedNumber from "@/components/AnimatedNumber";

function growLightLabel(on) {
  return on ? "LIGHT · UV ON" : "LIGHT LEVEL";
}

const stagger = {
  hidden: { opacity: 0, y: 16 },
  show: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.06, duration: 0.4, ease: "easeOut" },
  }),
};

function StatCard({ i, icon: Icon, label, value, unit, accent, sub, decimals = 0, raw }) {
  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      animate="show"
      custom={i}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="crt sheen relative rounded-xl border border-verde-border bg-verde-card p-4 transition-all duration-300 hover:shadow-glow"
    >
      <div className="flex items-center justify-between">
        <p className="text-[9px] tracking-widest text-verde-muted">{label}</p>
        <motion.span
          animate={{ scale: [1, 1.15, 1] }}
          transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.4 }}
        >
          <Icon size={14} style={{ color: accent }} />
        </motion.span>
      </div>
      <p className="mt-2 font-display text-2xl font-bold text-verde-text">
        {raw != null ? (
          raw
        ) : (
          <AnimatedNumber value={value} decimals={decimals} />
        )}
        <span className="ml-1 text-xs font-normal text-verde-muted">{unit}</span>
      </p>
      {sub && <p className="mt-1 text-[9px] text-verde-dim">{sub}</p>}
    </motion.div>
  );
}

export default function OverviewSection({ sensors, controls, online, scan }) {
  const pumpOn = !!controls.pump_state;
  const lightOn = !!controls.grow_light_state;
  const manual = !!controls.manual_mode;

  return (
    <div className="space-y-5">
      {/* Hero row: the two big instruments */}
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        <MoistureGauge
          value={sensors.moisture}
          threshold={controls.moisture_threshold}
        />
        <ReservoirCylinder value={sensors.tank_level} />
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard
          i={0}
          icon={Thermometer}
          label="AMBIENT TEMP"
          value={sensors.temperature ?? 0}
          decimals={1}
          unit="°C"
          accent="#f97316"
          sub="DHT22 · GPIO 4"
        />
        <StatCard
          i={1}
          icon={Droplet}
          label="AIR HUMIDITY"
          value={sensors.humidity ?? 0}
          decimals={1}
          unit="%"
          accent="#38bdf8"
          sub="DHT22 · GPIO 4"
        />
        <StatCard
          i={2}
          icon={SunMedium}
          label={growLightLabel(lightOn)}
          value={sensors.lux ?? 0}
          unit="LUX"
          accent={lightOn ? "#a855f7" : "#eab308"}
          sub={lightOn ? "UV GROW LIGHT ACTIVE" : "LDR · GPIO 35"}
        />
        <StatCard
          i={3}
          icon={Waves}
          label="MODE"
          raw={manual ? "MANUAL" : "AUTO"}
          unit=""
          accent="#22c55e"
          sub={manual ? "OPERATOR IN COMMAND" : "SMART BOTANIST ACTIVE"}
        />
      </div>

      {/* Live activity strip */}
      <motion.div
        variants={stagger}
        initial="hidden"
        animate="show"
        custom={4}
        className="crt relative rounded-lg border border-verde-border bg-verde-card p-4"
      >
        <p className="mb-3 text-[9px] tracking-widest text-verde-muted">
          ▓ LIVE ACTUATOR & EVENT STATUS
        </p>
        <div className="flex flex-wrap gap-3">
          <span
            className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[10px] ${
              pumpOn
                ? "border-verde-water/60 text-verde-water shadow-glow-water"
                : "border-verde-border text-verde-muted"
            }`}
          >
            <Droplet size={12} />
            PUMP {pumpOn ? "RUNNING" : "IDLE"}
          </span>
          <span
            className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[10px] ${
              lightOn
                ? "border-purple-500/60 text-purple-400"
                : "border-verde-border text-verde-muted"
            }`}
          >
            <Lightbulb size={12} />
            UV LIGHT {lightOn ? "ON · 395nm" : "OFF"}
          </span>
          <span
            className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[10px] ${
              controls.capture_photo
                ? "border-verde-green/60 text-verde-green shadow-glow-sm"
                : "border-verde-border text-verde-muted"
            }`}
          >
            <Camera size={12} />
            CAMERA {controls.capture_photo ? "CAPTURING…" : "IDLE"}
          </span>
          <span
            className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[10px] ${
              controls.weather_override === 1
                ? "border-verde-water/60 text-verde-water"
                : "border-verde-border text-verde-muted"
            }`}
          >
            <CloudRain size={12} />
            {controls.weather_override === 1
              ? "RAIN HOLD ACTIVE"
              : "NO WEATHER HOLD"}
          </span>
          <span
            className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[10px] ${
              manual
                ? "border-amber-500/60 text-amber-400"
                : "border-verde-green/40 text-verde-dim"
            }`}
          >
            {manual ? <Hand size={12} /> : <Bot size={12} />}
            {manual ? "MANUAL OVERRIDE" : "AUTONOMOUS"}
          </span>
        </div>
        {scan?.captured_at ? (
          <p className="mt-3 text-[9px] text-verde-muted">
            LAST FOLIAGE SCAN:{" "}
            {new Date(scan.captured_at).toLocaleString()} — see AI LAB section
          </p>
        ) : null}
      </motion.div>
    </div>
  );
}
