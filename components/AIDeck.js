"use client";
// AI Diagnostic Deck — "Scan Plant Foliage" trigger, captured photo
// viewport, and the Gemini monospace chatbot terminal.
// Flow: button -> capture_photo=true -> ESP32-CAM snaps -> /api/upload-photo
// resets flag + writes /latest_scan -> this deck calls /api/analyze-plant.
import { useEffect, useRef, useState } from "react";
/* eslint-disable @next/next/no-img-element */
import { motion, AnimatePresence } from "framer-motion";
import { Camera, Loader2, ScanLine, Terminal } from "lucide-react";

const SCAN_TIMEOUT_MS = 45000;

export default function AIDeck({ controls, requestCapture, scan, online }) {
  const [scanning, setScanning] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "system",
      text: "VERDE AI TERMINAL v3.0 — botanical diagnostics online. Click [SCAN PLANT FOLIAGE] to begin.",
    },
  ]);
  const [error, setError] = useState(null);
  const timeoutRef = useRef(null);
  const lastAnalyzedRef = useRef(null);
  const termRef = useRef(null);

  const pushMsg = (role, text) =>
    setMessages((m) => [...m, { role, text }]);

  // Auto-scroll terminal
  useEffect(() => {
    if (termRef.current)
      termRef.current.scrollTop = termRef.current.scrollHeight;
  }, [messages, analyzing]);

  // Scanning spinner is released when capture_photo flips back to false
  useEffect(() => {
    if (scanning && controls.capture_photo === false) {
      clearTimeout(timeoutRef.current);
      setScanning(false);
    }
  }, [controls.capture_photo, scanning]);

  // When a new scan lands in /latest_scan, run AI analysis exactly once
  useEffect(() => {
    const scanImage = scan?.imageUrl || scan?.imageDataUrl;
    if (!scanImage || scan.captured_at === lastAnalyzedRef.current) return;
    lastAnalyzedRef.current = scan.captured_at;

    const analyze = async () => {
      setAnalyzing(true);
      pushMsg("system", "> foliage scan received. uploading to Plant.id …");
      try {
        const res = await fetch("/api/analyze-plant", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            imageUrl: scan.imageUrl || undefined,
            imageDataUrl: scan.imageDataUrl || undefined,
          }),
        });
        const data = await res.json();
        if (!res.ok || !data.success) {
          throw new Error(data.error || `Analysis failed (${res.status})`);
        }
        pushMsg(
          "system",
          `> IDENTIFIED: ${data.plant_identified} · DIAGNOSIS: ${data.health_diagnosis}`
        );
        pushMsg("ai", data.gemini_remedy);
      } catch (err) {
        pushMsg("error", `✗ ${err.message}`);
      } finally {
        setAnalyzing(false);
      }
    };
    analyze();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scan]);

  const handleScan = async () => {
    if (scanning || !online) return;
    setError(null);
    setScanning(true);
    pushMsg("system", "> capture_photo=true written · waking vision node …");
    try {
      await requestCapture();
      timeoutRef.current = setTimeout(() => {
        setScanning(false);
        setError(
          "Scan Failed: camera node did not respond within 45s. Check power & Wi-Fi."
        );
        pushMsg("error", "✗ Scan timeout — insufficient power on camera node?");
      }, SCAN_TIMEOUT_MS);
    } catch {
      setScanning(false);
      setError("Could not write capture flag to Firebase.");
    }
  };

  return (
    <div className="crt relative rounded-lg border border-verde-border bg-verde-card p-5 transition-shadow hover:shadow-glow">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <p className="text-[10px] tracking-widest text-verde-muted">
          ▓ AI DIAGNOSTIC DECK · PLANT.ID + GEMINI 2.0 FLASH
        </p>
        <motion.button
          whileTap={{ scale: 0.96 }}
          onClick={handleScan}
          disabled={scanning || !online}
          className={`flex items-center gap-2 rounded border px-4 py-2 text-xs transition-all duration-200 ${
            scanning
              ? "cursor-wait border-verde-green/40 text-verde-dim"
              : !online
              ? "cursor-not-allowed border-verde-border text-verde-muted opacity-50"
              : "border-verde-green bg-verde-green/10 text-verde-green hover:bg-verde-green/20 hover:shadow-glow"
          }`}
        >
          {scanning ? (
            <>
              <Loader2 size={14} className="animate-spin" />
              CAPTURING — VISION NODE ACTIVE…
            </>
          ) : (
            <>
              <Camera size={14} />
              SCAN PLANT FOLIAGE
            </>
          )}
        </motion.button>
      </div>

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mb-3 rounded border border-verde-danger/50 bg-red-950/30 px-3 py-2 text-[10px] text-verde-danger"
          >
            ❌ {error}
          </motion.p>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Foliage viewport */}
        <div className="relative flex min-h-[240px] items-center justify-center overflow-hidden rounded border border-verde-border bg-verde-panel">
          {scan?.imageUrl || scan?.imageDataUrl ? (
            <>
              <img
                src={scan.imageUrl || scan.imageDataUrl}
                alt="Latest foliage scan"
                className="h-full w-full object-contain"
              />
              <div className="pointer-events-none absolute inset-0 overflow-hidden">
                <div className="h-8 w-full animate-scanline bg-gradient-to-b from-transparent via-verde-green/10 to-transparent" />
              </div>
              <p className="absolute bottom-2 left-2 rounded bg-verde-bg/80 px-2 py-0.5 text-[9px] text-verde-dim">
                CAPTURED{" "}
                {scan.captured_at
                  ? new Date(scan.captured_at).toLocaleTimeString()
                  : "—"}{" "}
                · OV2640 SVGA
              </p>
            </>
          ) : (
            <div className="flex flex-col items-center gap-2 text-verde-muted">
              <ScanLine size={28} />
              <p className="text-[10px]">NO FOLIAGE SCAN IN BUFFER</p>
            </div>
          )}
        </div>

        {/* Chatbot terminal */}
        <div className="flex min-h-[240px] flex-col overflow-hidden rounded border border-verde-border bg-[#070b07]">
          <div className="flex items-center gap-2 border-b border-verde-border px-3 py-1.5 text-[10px] text-verde-dim">
            <Terminal size={11} />
            verde-ai@plant-os:~$
          </div>
          <div
            ref={termRef}
            className="flex-1 space-y-2 overflow-y-auto p-3 text-[11px] leading-relaxed"
          >
            {messages.map((m, i) => (
              <p
                key={i}
                className={
                  m.role === "ai"
                    ? "whitespace-pre-wrap text-verde-green"
                    : m.role === "error"
                    ? "text-verde-danger"
                    : "text-verde-dim"
                }
              >
                {m.text}
              </p>
            ))}
            {analyzing && (
              <p className="text-verde-green">
                analyzing foliage<span className="animate-blink">▌</span>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
