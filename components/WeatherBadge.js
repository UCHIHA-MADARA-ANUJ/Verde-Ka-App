"use client";
// Delhi weather badge fed from /weather (written by /api/weather-sync).
import { useEffect, useState } from "react";
import { onValue } from "firebase/database";
import { verdeRef } from "@/lib/firebase";
import { demoSubscribe } from "@/lib/demoStore";
import { CloudRain, Sun, Cloud, CloudLightning } from "lucide-react";

function iconFor(condition) {
  const c = (condition || "").toLowerCase();
  if (c.includes("thunder")) return CloudLightning;
  if (c.includes("rain") || c.includes("drizzle")) return CloudRain;
  if (c.includes("cloud")) return Cloud;
  return Sun;
}

export default function WeatherBadge({ enabled, demo = false, weatherOverride }) {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    if (demo) {
      const unsub = demoSubscribe((snap) => setWeather(snap.weather));
      return unsub;
    }
    if (!enabled) return;
    const weatherRef = verdeRef("/weather");
    if (!weatherRef) return;
    const unsub = onValue(
      weatherRef,
      (snap) => setWeather(snap.val()),
      () => {}
    );
    return () => unsub();
  }, [enabled, demo]);

  const condition = weather?.condition || "—";
  const Icon = iconFor(condition);
  const rainy = weatherOverride === 1;

  return (
    <div
      className={`flex items-center gap-2 rounded border px-3 py-1.5 text-[11px] ${
        rainy
          ? "border-verde-water/60 text-verde-water shadow-glow-water"
          : "border-verde-border bg-verde-panel text-verde-text"
      }`}
    >
      <Icon size={13} />
      <span>
        DELHI: {condition.toUpperCase()}
        {weather?.temp != null && ` · ${Math.round(weather.temp)}°C`}
      </span>
      {rainy && <span className="text-verde-water">· IRRIGATION SUSPENDED</span>}
    </div>
  );
}
