"use client";
// ============================================================
// VERDE TECH V3.0 — SECTIONED CONTROL DECK
// Sidebar navigation: OVERVIEW · TELEMETRY · CONTROLS · AI LAB · SYSTEM
// Cinematic boot loader on entry. Live Firebase RTDB throughout.
// ============================================================
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { useVerdeSession } from "@/lib/hooks/useVerdeSession";
import { useTelemetry } from "@/lib/hooks/useTelemetry";
import { useControls } from "@/lib/hooks/useControls";
import { useMoistureHistory } from "@/lib/hooks/useMoistureHistory";
import { useLatestScan } from "@/lib/hooks/useLatestScan";

import BootLoader from "@/components/BootLoader";
import Sidebar, { SECTIONS } from "@/components/Sidebar";
import StatusBadge from "@/components/StatusBadge";
import WeatherBadge from "@/components/WeatherBadge";
import Toasts from "@/components/Toasts";

import OverviewSection from "@/components/sections/OverviewSection";
import TelemetrySection from "@/components/sections/TelemetrySection";
import ControlsSection from "@/components/sections/ControlsSection";
import AILabSection from "@/components/sections/AILabSection";
import SystemSection from "@/components/sections/SystemSection";

export default function Dashboard() {
  const { status: sessionStatus } = useVerdeSession();
  const ready = sessionStatus === "ready";
  const settled = sessionStatus !== "connecting";

  const { sensors, online, hasData } = useTelemetry(ready);
  const { controls, setControl, requestCapture } = useControls(ready);
  const points = useMoistureHistory(ready, sensors.moisture, hasData);
  const scan = useLatestScan(ready);

  const [section, setSection] = useState("overview");
  const activeMeta = SECTIONS.find((s) => s.id === section);

  return (
    <div className="min-h-screen bg-verde-bg">
      <BootLoader done={settled} />

      <Sidebar active={section} onSelect={setSection} online={online} />

      {/* Main content area */}
      <main className="px-4 pb-24 pt-6 sm:px-6 lg:ml-56 lg:pb-10">
        {/* Top bar */}
        <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-lg tracking-widest text-verde-green text-glow">
              {activeMeta?.label}
            </h1>
            <p className="text-[9px] tracking-[0.3em] text-verde-muted">
              VERDE CONTROL DECK · AUTONOMOUS PLANT OS
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {section !== "controls" && (
              <WeatherBadge
                enabled={ready}
                weatherOverride={controls.weather_override}
              />
            )}
            <StatusBadge
              sessionStatus={sessionStatus}
              online={online}
              hasData={hasData}
            />
          </div>
        </header>

        {/* Config / error banners */}
        {sessionStatus === "unconfigured" && (
          <div className="mb-6 rounded border border-amber-500/50 bg-amber-950/20 px-4 py-3 text-[11px] text-amber-400">
            ⚠ FIREBASE NOT CONFIGURED — paste your web app keys into{" "}
            <span className="text-amber-200">lib/firebaseConfig.js</span> (or
            set NEXT_PUBLIC_FIREBASE_* env vars) and redeploy.
          </div>
        )}
        {sessionStatus === "error" && (
          <div className="mb-6 rounded border border-verde-danger bg-red-950/30 px-4 py-3 text-[11px] text-verde-danger">
            ❌ Connection Failed: security token rejected. Verify Anonymous
            Auth is enabled and this domain is in Firebase → Authentication →
            Authorized domains.
          </div>
        )}

        {/* Section router with slide transitions */}
        <AnimatePresence mode="wait">
          <motion.div
            key={section}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.28, ease: "easeOut" }}
          >
            {section === "overview" && (
              <OverviewSection
                sensors={sensors}
                controls={controls}
                online={online}
                scan={scan}
              />
            )}
            {section === "telemetry" && (
              <TelemetrySection
                sensors={sensors}
                points={points}
                threshold={controls.moisture_threshold}
              />
            )}
            {section === "controls" && (
              <ControlsSection
                controls={controls}
                setControl={setControl}
                online={online}
                sensors={sensors}
                sessionReady={ready}
              />
            )}
            {section === "ailab" && (
              <AILabSection
                controls={controls}
                requestCapture={requestCapture}
                scan={scan}
                online={online}
              />
            )}
            {section === "system" && (
              <SystemSection
                online={online}
                sensors={sensors}
                controls={controls}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </main>

      <Toasts sensors={sensors} controls={controls} />
    </div>
  );
}
