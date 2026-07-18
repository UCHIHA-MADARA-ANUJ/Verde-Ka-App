"use client";
// Ambient metric cards: temperature, humidity, light level.
import { Thermometer, Droplets, SunMedium } from "lucide-react";

function Card({ icon: Icon, label, value, unit, accent }) {
  return (
    <div className="crt relative flex items-center gap-3 rounded-lg border border-verde-border bg-verde-card p-4 transition-shadow hover:shadow-glow">
      <div
        className="rounded border border-verde-border p-2"
        style={{ color: accent }}
      >
        <Icon size={18} />
      </div>
      <div>
        <p className="text-[9px] tracking-widest text-verde-muted">{label}</p>
        <p className="text-xl text-verde-text">
          {value}
          <span className="ml-1 text-xs text-verde-muted">{unit}</span>
        </p>
      </div>
    </div>
  );
}

export default function TelemetryCards({ sensors, growLightOn }) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 lg:grid-cols-1">
      <Card
        icon={Thermometer}
        label="AMBIENT TEMP"
        value={Number(sensors.temperature ?? 0).toFixed(1)}
        unit="°C"
        accent="#f97316"
      />
      <Card
        icon={Droplets}
        label="AIR HUMIDITY"
        value={Number(sensors.humidity ?? 0).toFixed(1)}
        unit="%"
        accent="#38bdf8"
      />
      <Card
        icon={SunMedium}
        label={growLightOn ? "LIGHT · UV GROW ON" : "LIGHT LEVEL"}
        value={sensors.lux ?? 0}
        unit="LUX"
        accent={growLightOn ? "#a855f7" : "#eab308"}
      />
    </div>
  );
}
