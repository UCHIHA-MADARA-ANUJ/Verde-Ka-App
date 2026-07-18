"use client";
// ============================================================
// useControls — bi-directional sync with /controls.
// Reads live control state and exposes setters that write
// straight back to Firebase RTDB (sub-100ms round trip).
// In demo mode, reads/writes go to the local simulation engine.
// ============================================================
import { useEffect, useState, useCallback } from "react";
import { onValue, update, set } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import {
  demoSubscribe,
  demoSetControl,
  demoRequestCapture,
} from "@/lib/demoStore";
import { PATHS, CONTROL_DEFAULTS } from "@/lib/paths";

export function useControls(enabled, demo = false) {
  const [controls, setControls] = useState(CONTROL_DEFAULTS);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (demo) {
      const unsub = demoSubscribe((snap) => {
        setControls((prev) => ({ ...prev, ...snap.controls }));
        setLoaded(true);
      });
      return unsub;
    }
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
  }, [enabled, demo]);

  /** Patch one or more control fields (optimistic local update). */
  const setControl = useCallback(
    async (patch) => {
      if (demo) {
        demoSetControl(patch);
        return;
      }
      setControls((prev) => ({ ...prev, ...patch }));
      try {
        const controlsRef = verdeRef(PATHS.CONTROLS);
        if (!controlsRef) throw new Error("Firebase not configured");
        await update(controlsRef, patch);
      } catch (err) {
        console.error("Control write failed:", err);
      }
    },
    [demo]
  );

  /** Fire the camera capture flag. */
  const requestCapture = useCallback(async () => {
    if (demo) return demoRequestCapture();
    try {
      const flagRef = verdeRef(`${PATHS.CONTROLS}/capture_photo`);
      if (!flagRef) throw new Error("Firebase not configured");
      await set(flagRef, true);
    } catch (err) {
      console.error("Capture trigger failed:", err);
      throw err;
    }
  }, [demo]);

  return { controls, loaded, setControl, requestCapture };
}
