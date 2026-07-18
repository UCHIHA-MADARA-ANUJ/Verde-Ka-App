"use client";
// ============================================================
// SIDEBAR — section navigation for the Verde Control Deck.
// Desktop: fixed left rail. Mobile: bottom tab bar.
// ============================================================
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Activity,
  SlidersHorizontal,
  Sparkles,
  ServerCog,
  Sprout,
} from "lucide-react";

export const SECTIONS = [
  { id: "overview", label: "OVERVIEW", icon: LayoutDashboard },
  { id: "telemetry", label: "TELEMETRY", icon: Activity },
  { id: "controls", label: "CONTROLS", icon: SlidersHorizontal },
  { id: "ailab", label: "AI LAB", icon: Sparkles },
  { id: "system", label: "SYSTEM", icon: ServerCog },
];

export default function Sidebar({ active, onSelect, online }) {
  return (
    <>
      {/* ── Desktop rail ── */}
      <aside className="fixed left-0 top-0 z-40 hidden h-screen w-56 flex-col border-r border-verde-border bg-verde-panel/80 backdrop-blur lg:flex">
        <div className="flex items-center gap-3 border-b border-verde-border px-5 py-5">
          <motion.div
            animate={{
              boxShadow: [
                "0 0 8px rgba(34,197,94,0.25)",
                "0 0 18px rgba(34,197,94,0.6)",
                "0 0 8px rgba(34,197,94,0.25)",
              ],
            }}
            transition={{ duration: 2.5, repeat: Infinity }}
            className="rounded-lg border border-verde-green/40 p-2 text-verde-green"
          >
            <motion.span
              animate={{ rotate: [0, 8, -8, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
              className="block"
            >
              <Sprout size={18} />
            </motion.span>
          </motion.div>
          <div>
            <p className="font-display text-sm font-bold tracking-widest text-verde-green text-glow">
              VERDE
            </p>
            <p className="text-[8px] tracking-[0.3em] text-verde-muted">
              PLANT OS v3.0
            </p>
          </div>
        </div>

        <nav className="flex-1 space-y-1 p-3">
          {SECTIONS.map((s) => {
            const Icon = s.icon;
            const isActive = active === s.id;
            return (
              <button
                key={s.id}
                onClick={() => onSelect(s.id)}
                className={`relative flex w-full items-center gap-3 rounded px-4 py-3 text-left text-[11px] tracking-widest transition-all duration-200 ${
                  isActive
                    ? "text-verde-green"
                    : "text-verde-muted hover:bg-verde-card hover:text-verde-text"
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="nav-pill"
                    className="absolute inset-0 rounded border border-verde-green/40 bg-verde-green/10 shadow-glow-sm"
                    transition={{ type: "spring", stiffness: 400, damping: 32 }}
                  />
                )}
                <Icon size={15} className="relative z-10" />
                <span className="relative z-10">{s.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="border-t border-verde-border p-4">
          <div className="flex items-center gap-2 text-[9px]">
            <span
              className={`h-2 w-2 rounded-full ${
                online
                  ? "bg-verde-green shadow-glow-sm"
                  : "bg-verde-danger animate-pulse"
              }`}
            />
            <span className={online ? "text-verde-dim" : "text-verde-danger"}>
              {online ? "EDGE NODE ONLINE" : "EDGE NODE OFFLINE"}
            </span>
          </div>
          <p className="mt-2 text-[8px] leading-relaxed text-verde-muted">
            ESP32 WROOM-32 + ESP32-CAM
            <br />
            DAV ACON 5 · DELHI, IN
          </p>
        </div>
      </aside>

      {/* ── Mobile bottom tab bar ── */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 flex border-t border-verde-border bg-verde-panel/95 backdrop-blur lg:hidden">
        {SECTIONS.map((s) => {
          const Icon = s.icon;
          const isActive = active === s.id;
          return (
            <button
              key={s.id}
              onClick={() => onSelect(s.id)}
              className={`flex flex-1 flex-col items-center gap-1 py-2.5 text-[8px] tracking-wider transition-colors ${
                isActive ? "text-verde-green" : "text-verde-muted"
              }`}
            >
              <Icon size={16} />
              {s.label}
              {isActive && (
                <motion.div
                  layoutId="nav-dot"
                  className="h-0.5 w-8 rounded-full bg-verde-green shadow-glow-sm"
                />
              )}
            </button>
          );
        })}
      </nav>
    </>
  );
}
