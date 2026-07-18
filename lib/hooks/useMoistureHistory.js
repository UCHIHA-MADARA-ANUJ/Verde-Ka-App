"use client";
// ============================================================
// useMoistureHistory — streams /historical_logs/moisture_log and
// also appends a live in-memory point every time moisture changes,
// so the chart animates even before the ESP32 writes history nodes.
// Keeps the last 24 hours of points, capped at 500 entries.
// ============================================================
import { useEffect, useRef, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { PATHS } from "@/lib/paths";

const DAY_MS = 24 * 60 * 60 * 1000;
const MAX_POINTS = 500;

function fmtTime(ts) {
  const d = new Date(ts);
  return `${String(d.getHours()).padStart(2, "0")}:${String(
    d.getMinutes()
  ).padStart(2, "0")}`;
}

export function useMoistureHistory(enabled, liveMoisture, hasData, demo = false) {
  const [points, setPoints] = useState([]);
  const livePointsRef = useRef([]);
  const dbPointsRef = useRef([]);

  const merge = () => {
    const cutoff = Date.now() - DAY_MS;
    const all = [...dbPointsRef.current, ...livePointsRef.current]
      .filter((p) => p.ts >= cutoff)
      .sort((a, b) => a.ts - b.ts)
      .slice(-MAX_POINTS);
    setPoints(all);
  };

  // Historical log subscription (skipped in demo — live points only)
  useEffect(() => {
    if (!enabled || demo) return;
    const logRef = verdeRef(PATHS.MOISTURE_LOG);
    if (!logRef) return;
    const unsub = onValue(
      logRef,
      (snap) => {
        const val = snap.val() || {};
        dbPointsRef.current = Object.entries(val).map(([k, v]) => {
          let ts = Number(k);
          if (ts < 1e12) ts *= 1000; // epoch seconds -> ms
          return { ts, time: fmtTime(ts), moisture: Number(v) };
        });
        merge();
      },
      () => {}
    );
    return () => unsub();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled]);

  // Live appender — every 15s (4s in demo so the chart fills fast)
  useEffect(() => {
    if (!enabled || !hasData) return;
    const minGap = demo ? 4000 : 15000;
    const now = Date.now();
    const last = livePointsRef.current[livePointsRef.current.length - 1];
    if (last && now - last.ts < minGap) return;
    livePointsRef.current.push({
      ts: now,
      time: fmtTime(now),
      moisture: liveMoisture,
    });
    if (livePointsRef.current.length > MAX_POINTS) {
      livePointsRef.current = livePointsRef.current.slice(-MAX_POINTS);
    }
    merge();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, liveMoisture, hasData]);

  return points;
}
