"use client";
// ============================================================
// useVerdeSession — boots Anonymous Auth on dashboard load.
// status: 'connecting' | 'ready' | 'demo' | 'error'
// If Firebase env vars are absent → 'demo' (local simulation mode,
// zero setup required; also the exhibition Wi-Fi-failure fallback).
// ============================================================
import { useEffect, useState } from "react";
import { initializeUserSession, isFirebaseConfigured } from "@/lib/firebase";

export function useVerdeSession() {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState("connecting");

  useEffect(() => {
    let mounted = true;

    if (!isFirebaseConfigured()) {
      setStatus("demo");
      return () => {};
    }

    initializeUserSession().then((u) => {
      if (!mounted) return;
      if (u) {
        setUser(u);
        setStatus("ready");
      } else {
        setStatus("error");
      }
    });
    return () => {
      mounted = false;
    };
  }, []);

  return { user, status };
}
