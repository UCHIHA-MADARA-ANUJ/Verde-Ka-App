"use client";
// ============================================================
// useControls — bi-directional /controls sync (<100ms writes).
// ============================================================
import { useEffect, useState, useCallback } from "react";
import { onValue, update, set } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { PATHS, CONTROL_DEFAULTS } from "@/lib/paths";

export function useControls(enabled) {
  const [controls, setControls] = useState(CONTROL_DEFAULTS);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!enabled) return;
    const controlsRef = verdeRef(PATHS.CONTROLS);
    if (!controlsRef) return;
    const unsub = onValue(
      controlsRef,
      (snap) => {
        const val = snap.val();
        if (val) setControls((prev) => ({ ...prev, ...val }));
        setLoaded(true);
      },
      (err) => console.error("Controls stream error:", err)
    );
    return () => unsub();
  }, [enabled]);

  const setControl = useCallback(async (patch) => {
    setControls((prev) => ({ ...prev, ...patch }));
    try {
      const controlsRef = verdeRef(PATHS.CONTROLS);
      if (!controlsRef) throw new Error("Firebase not configured");
      await update(controlsRef, patch);
    } catch (err) {
      console.error("Control write failed:", err);
    }
  }, []);

  const requestCapture = useCallback(async () => {
    const flagRef = verdeRef(`${PATHS.CONTROLS}/capture_photo`);
    if (!flagRef) throw new Error("Firebase not configured");
    await set(flagRef, true);
  }, []);

  return { controls, loaded, setControl, requestCapture };
}
