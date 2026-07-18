"use client";
// Device state badge — ONLINE / OFFLINE / CONNECTING with pulse states.
import { motion } from "framer-motion";
import { Wifi, WifiOff, Loader2 } from "lucide-react";

export default function StatusBadge({ sessionStatus, online, hasData }) {
  let label, cls, Icon, spin = false;

  if (sessionStatus === "connecting") {
    label = "CONNECTING…";
    cls = "border-yellow-500/50 text-yellow-400";
    Icon = Loader2;
    spin = true;
  } else if (sessionStatus === "demo") {
    label = "DEMO MODE · SIMULATED EDGE";
    cls = "border-purple-500/60 text-purple-400";
    Icon = Wifi;
  } else if (sessionStatus === "error") {
    label = "AUTH FAILED — RETRY";
    cls = "border-verde-danger text-verde-danger animate-pulse-red";
    Icon = WifiOff;
  } else if (online) {
    label = "EDGE ONLINE";
    cls = "border-verde-green/60 text-verde-green shadow-glow-sm";
    Icon = Wifi;
  } else if (hasData) {
    label = "EDGE OFFLINE · AUTONOMOUS MODE";
    cls = "border-verde-danger text-verde-danger animate-pulse-red";
    Icon = WifiOff;
  } else {
    label = "AWAITING TELEMETRY…";
    cls = "border-verde-border text-verde-muted";
    Icon = Loader2;
    spin = true;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-center gap-2 rounded border bg-verde-panel px-3 py-1.5 text-[11px] ${cls}`}
    >
      <Icon size={13} className={spin ? "animate-spin" : ""} />
      {label}
    </motion.div>
  );
}
