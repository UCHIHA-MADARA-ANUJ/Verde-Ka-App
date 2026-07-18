"use client";
// ============================================================
// useTelemetry — opens a permanent WebSocket stream to /sensors.
// Also derives the device online/offline state:
// If last_updated is older than 10s → "EDGE OFFLINE" (cached values kept).
// In demo mode, subscribes to the local simulation engine instead.
// ============================================================
import { useEffect, useRef, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { demoSubscribe } from "@/lib/demoStore";
import { PATHS, SENSOR_DEFAULTS, OFFLINE_TIMEOUT_MS } from "@/lib/paths";

export function useTelemetry(enabled, demo = false) {
  const [sensors, setSensors] = useState(SENSOR_DEFAULTS);
  const [online, setOnline] = useState(false);
  const [hasData, setHasData] = useState(false);
  const lastEventRef = useRef(0);

  // Live subscription — Firebase or demo engine
  useEffect(() => {
    if (demo) {
      const unsub = demoSubscribe((snap) => {
        setSensors((prev) => ({ ...prev, ...snap.sensors }));
        setHasData(true);
        lastEventRef.current = Date.now();
        setOnline(true);
      });
      return unsub;
    }
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
      (err) => {
        console.error("Telemetry stream error:", err);
      }
    );
    return () => unsub();
  }, [enabled, demo]);

  // Watchdog: mark offline when no fresh writes arrive within 10s
  useEffect(() => {
    if (!enabled && !demo) return;
    const t = setInterval(() => {
      const stale = Date.now() - lastEventRef.current > OFFLINE_TIMEOUT_MS;
      setOnline(!stale && lastEventRef.current !== 0);
    }, 2000);
    return () => clearInterval(t);
  }, [enabled, demo]);

  return { sensors, online, hasData };
}
