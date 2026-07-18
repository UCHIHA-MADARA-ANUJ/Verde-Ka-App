"use client";
// ============================================================
// useTelemetry — permanent WebSocket stream to /sensors with a
// 10s last-write watchdog deriving EDGE ONLINE/OFFLINE state.
// ============================================================
import { useEffect, useRef, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { PATHS, SENSOR_DEFAULTS, OFFLINE_TIMEOUT_MS } from "@/lib/paths";

export function useTelemetry(enabled) {
  const [sensors, setSensors] = useState(SENSOR_DEFAULTS);
  const [online, setOnline] = useState(false);
  const [hasData, setHasData] = useState(false);
  const lastEventRef = useRef(0);

  useEffect(() => {
    if (!enabled) return;
    const sensorsRef = verdeRef(PATHS.SENSORS);
    if (!sensorsRef) return;
    const unsub = onValue(
      sensorsRef,
      (snap) => {
        const val = snap.val();
        if (val) {
          setSensors((prev) => ({ ...prev, ...val }));
          setHasData(true);
          lastEventRef.current = Date.now();
          setOnline(true);
        }
      },
      (err) => console.error("Telemetry stream error:", err)
    );
    return () => unsub();
  }, [enabled]);

  useEffect(() => {
    if (!enabled) return;
    const t = setInterval(() => {
      const stale = Date.now() - lastEventRef.current > OFFLINE_TIMEOUT_MS;
      setOnline(!stale && lastEventRef.current !== 0);
    }, 2000);
    return () => clearInterval(t);
  }, [enabled]);

  return { sensors, online, hasData };
}
