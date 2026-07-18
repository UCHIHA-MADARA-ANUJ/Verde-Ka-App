"use client";
// In-app toast alerts per App/13_Notifications.md:
// - Grow light activated (lux < 400)
// - Irrigation complete (+5% moisture after watering)
// - Reservoir critical modal handled by ReservoirCylinder card
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

let idSeq = 0;

export default function Toasts({ sensors, controls }) {
  const [toasts, setToasts] = useState([]);
  const prevLight = useRef(false);
  const pumpBaseline = useRef(null);
  const prevPump = useRef(false);

  const push = (text, tone = "green") => {
    const id = ++idSeq;
    setToasts((t) => [...t, { id, text, tone }]);
    setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, 5000);
  };

  // Grow light activation toast
  useEffect(() => {
    const on = !!controls.grow_light_state;
    if (on && !prevLight.current) {
      push("☀️ GROW LIGHT ACTIVATED: 5mm UV LED turned ON.");
    }
    prevLight.current = on;
  }, [controls.grow_light_state]);

  // Irrigation success toast (+5% moisture after a pump run)
  useEffect(() => {
    const pumpOn = !!controls.pump_state;
    if (pumpOn && !prevPump.current) {
      pumpBaseline.current = sensors.moisture;
    }
    if (
      !pumpOn &&
      prevPump.current &&
      pumpBaseline.current != null &&
      sensors.moisture - pumpBaseline.current >= 5
    ) {
      push("💧 IRRIGATION COMPLETE: plant successfully watered.");
      pumpBaseline.current = null;
    }
    prevPump.current = pumpOn;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [controls.pump_state, sensors.moisture]);

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      <AnimatePresence>
        {toasts.map((t) => (
          <motion.div
            key={t.id}
            initial={{ opacity: 0, x: 80, scale: 0.85 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 80, scale: 0.85 }}
            transition={{ type: "spring", stiffness: 320, damping: 24 }}
            className={`rounded-lg border px-4 py-2.5 text-[11px] shadow-glow-sm backdrop-blur ${
              t.tone === "green"
                ? "border-verde-green/50 bg-verde-panel text-verde-green"
                : "border-verde-water/50 bg-verde-panel text-verde-water"
            }`}
          >
            {t.text}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
