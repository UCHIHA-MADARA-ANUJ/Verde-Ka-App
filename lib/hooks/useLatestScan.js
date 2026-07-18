"use client";
// useLatestScan — watches /latest_scan for the newest leaf photo.
import { useEffect, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { PATHS } from "@/lib/paths";

export function useLatestScan(enabled) {
  const [scan, setScan] = useState(null);

  useEffect(() => {
    if (!enabled) return;
    const scanRef = verdeRef(PATHS.LATEST_SCAN);
    if (!scanRef) return;
    const unsub = onValue(
      scanRef,
      (snap) => setScan(snap.val() || null),
      () => {}
    );
    return () => unsub();
  }, [enabled]);

  return scan;
}
