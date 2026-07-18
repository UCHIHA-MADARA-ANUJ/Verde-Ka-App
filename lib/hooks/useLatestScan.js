"use client";
// ============================================================
// useLatestScan — watches /latest_scan for the newest uploaded
// leaf photo URL + AI diagnosis written by the backend routes.
// In demo mode, watches the local simulation engine instead.
// ============================================================
import { useEffect, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { demoSubscribe } from "@/lib/demoStore";
import { PATHS } from "@/lib/paths";

export function useLatestScan(enabled, demo = false) {
  const [scan, setScan] = useState(null);

  useEffect(() => {
    if (demo) {
      const unsub = demoSubscribe((snap) => setScan(snap.latest_scan));
      return unsub;
    }
    if (!enabled) return;
    const scanRef = verdeRef(PATHS.LATEST_SCAN);
    if (!scanRef) return;
    const unsub = onValue(
      scanRef,
      (snap) => setScan(snap.val() || null),
      () => {}
    );
    return () => unsub();
  }, [enabled, demo]);

  return scan;
}
