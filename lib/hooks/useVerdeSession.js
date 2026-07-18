"use client";
// ============================================================
// useVerdeSession — boots Anonymous Auth on dashboard load.
// status: 'connecting' | 'ready' | 'unconfigured' | 'error'
// ============================================================
import { useEffect, useState } from "react";
import { initializeUserSession, isFirebaseConfigured } from "@/lib/firebase";

export function useVerdeSession() {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState("connecting");

  useEffect(() => {
    let mounted = true;

    if (!isFirebaseConfigured()) {
      setStatus("unconfigured");
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
