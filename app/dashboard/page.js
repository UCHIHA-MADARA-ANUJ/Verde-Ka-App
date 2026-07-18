"use client";
// ============================================================
// VERDE TECH V3.0 — MAIN CONTROL DECK (single-page dashboard)
// Layout per App/14_UI_UX_Guidelines.md:
//   Row A  : status + weather badges
//   Cols   : telemetry (4) · history chart (5) · override deck (3)
//   Row B  : AI diagnostic deck (12)
// ============================================================
import dynamic from "next/dynamic";
import { motion } from "framer-motion";
import { Sprout } from "lucide-react";

import { useVerdeSession } from "@/lib/hooks/useVerdeSession";
import { useTelemetry } from "@/lib/hooks/useTelemetry";
import { useControls } from "@/lib/hooks/useControls";
import { useMoistureHistory } from "@/lib/hooks/useMoistureHistory";
import { useLatestScan } from "@/lib/hooks/useLatestScan";

import StatusBadge from "@/components/StatusBadge";
import WeatherBadge from "@/components/WeatherBadge";
import MoistureGauge from "@/components/MoistureGauge";
import ReservoirCylinder from "@/components/ReservoirCylinder";
import TelemetryCards from "@/components/TelemetryCards";
import ControlDeck from "@/components/ControlDeck";
import AIDeck from "@/components/AIDeck";
import Toasts from "@/components/Toasts";

// Lazy-load the heavy Recharts bundle (doc 16: performance)
const MoistureChart = dynamic(() => import("@/components/MoistureChart"), {
  ssr: false,
  loading: () => (
    <div className="flex min-h-[280px] items-center justify-center rounded-lg border border-verde-border bg-verde-card text-[11px] text-verde-muted">
      LOADING CHART MODULE…
    </div>
  ),
});

const fadeUp = {
  hidden: { opacity: 0, y: 14 },
  show: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.07, duration: 0.4, ease: "easeOut" },
  }),
};

export default function Dashboard() {
  const { status: sessionStatus } = useVerdeSession();
  const demo = sessionStatus === "demo";
  const ready = sessionStatus === "ready";
  const active = ready || demo;

  const { sensors, online, hasData } = useTelemetry(ready, demo);
  const { controls, setControl, requestCapture } = useControls(ready, demo);
  const points = useMoistureHistory(active, sensors.moisture, hasData, demo);
  const scan = useLatestScan(ready, demo);

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-4 py-6 sm:px-6">
      {/* ───────── Header ───────── */}
      <motion.header
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="mb-6 flex flex-wrap items-center justify-between gap-3"
      >
        <div className="flex items-center gap-3">
          <div className="rounded border border-verde-green/40 p-2 text-verde-green shadow-glow-sm">
            <Sprout size={20} />
          </div>
          <div>
            <h1 className="text-lg text-verde-green text-glow sm:text-xl">
              VERDE CONTROL DECK
            </h1>
            <p className="text-[9px] tracking-widest text-verde-muted">
              AUTONOMOUS PLANT OS · V3.0 · DAV ACON 5
            </p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <WeatherBadge
            enabled={ready}
            demo={demo}
            weatherOverride={controls.weather_override}
          />
          <StatusBadge
            sessionStatus={sessionStatus}
            online={online}
            hasData={hasData}
          />
        </div>
      </motion.header>

      {demo && (
        <div className="mb-6 rounded border border-purple-500/40 bg-purple-950/20 px-4 py-3 text-[11px] text-purple-300">
          ◈ DEMO MODE — Firebase env vars not detected. Running a full local
          ESP32 simulation (moisture decay, pump physics, day/night lux,
          simulated camera + canned Verde AI diagnosis). Add keys from{" "}
          <span className="text-purple-200">.env.example</span> to go live.
        </div>
      )}

      {sessionStatus === "error" && (
        <div className="mb-6 rounded border border-verde-danger bg-red-950/30 px-4 py-3 text-xs text-verde-danger">
          ❌ Connection Failed: Security token rejected. Check Firebase env
          config and allowed domains, then reload.
        </div>
      )}

      {/* ───────── Main grid ───────── */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        {/* Left — live telemetry (4 cols) */}
        <motion.section
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0}
          className="space-y-4 lg:col-span-4"
        >
          <MoistureGauge
            value={sensors.moisture}
            threshold={controls.moisture_threshold}
          />
          <ReservoirCylinder value={sensors.tank_level} />
        </motion.section>

        {/* Center — chart + ambient cards (5 cols) */}
        <motion.section
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={1}
          className="space-y-4 lg:col-span-5"
        >
          <MoistureChart
            points={points}
            threshold={controls.moisture_threshold}
          />
          <TelemetryCards
            sensors={sensors}
            growLightOn={!!controls.grow_light_state}
          />
        </motion.section>

        {/* Right — override deck (3 cols) */}
        <motion.section
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={2}
          className="lg:col-span-3"
        >
          <ControlDeck
            controls={controls}
            setControl={setControl}
            online={online}
            tankLevel={sensors.tank_level}
          />
        </motion.section>

        {/* Bottom — AI deck (12 cols) */}
        <motion.section
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={3}
          className="lg:col-span-12"
        >
          <AIDeck
            controls={controls}
            requestCapture={requestCapture}
            scan={scan}
            online={online}
            demo={demo}
          />
        </motion.section>
      </div>

      <footer className="mt-8 border-t border-verde-border pt-4 text-center text-[9px] text-verde-muted">
        PROJECT VERDE V3.0 · ESP32 WROOM-32 MAIN BRAIN + ESP32-CAM VISION NODE
        · FIREBASE RTDB SYNC &lt;100MS · BUILT BY AARAV &amp; ANUJ
      </footer>

      <Toasts sensors={sensors} controls={controls} />
    </main>
  );
}
