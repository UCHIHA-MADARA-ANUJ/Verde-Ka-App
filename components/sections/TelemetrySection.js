"use client";
// ═══ SECTION: TELEMETRY — full-width history chart + sensor detail table ═══
import dynamic from "next/dynamic";
import { motion } from "framer-motion";

const MoistureChart = dynamic(() => import("@/components/MoistureChart"), {
  ssr: false,
  loading: () => (
    <div className="flex min-h-[320px] items-center justify-center rounded-lg border border-verde-border bg-verde-card text-[11px] text-verde-muted">
      <span className="animate-pulse">LOADING CHART MODULE…</span>
    </div>
  ),
});

const SENSOR_ROWS = (s) => [
  {
    name: "SOIL MOISTURE",
    value: `${s.moisture ?? 0} %`,
    sensor: "2-Prong Resistive Probe (power-gated)",
    pin: "AO→GPIO34 · VCC→GPIO23",
    range: "0 – 100 %",
  },
  {
    name: "AMBIENT TEMPERATURE",
    value: `${Number(s.temperature ?? 0).toFixed(1)} °C`,
    sensor: "DHT22 / AM2302 digital bus",
    pin: "DATA→GPIO4",
    range: "-40 – 80 °C",
  },
  {
    name: "AIR HUMIDITY",
    value: `${Number(s.humidity ?? 0).toFixed(1)} %`,
    sensor: "DHT22 / AM2302 digital bus",
    pin: "DATA→GPIO4",
    range: "0 – 100 %",
  },
  {
    name: "LIGHT LEVEL",
    value: `${s.lux ?? 0} LUX`,
    sensor: "LDR analog divider",
    pin: "AO→GPIO35",
    range: "100 – 1200 LUX",
  },
  {
    name: "RESERVOIR LEVEL",
    value: `${s.tank_level ?? 0} %`,
    sensor: "HC-SR04 40kHz sonar",
    pin: "TRIG→GPIO18 · ECHO→GPIO19",
    range: "0 – 100 %",
  },
];

export default function TelemetrySection({ sensors, points, threshold }) {
  const lastUpdate = sensors.last_updated
    ? new Date(
        sensors.last_updated < 1e12
          ? sensors.last_updated * 1000
          : sensors.last_updated
      ).toLocaleTimeString()
    : "—";

  return (
    <div className="space-y-5">
      <MoistureChart points={points} threshold={threshold} />

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="crt relative overflow-hidden rounded-lg border border-verde-border bg-verde-card"
      >
        <div className="flex items-center justify-between border-b border-verde-border px-5 py-3">
          <p className="text-[9px] tracking-widest text-verde-muted">
            ▓ SENSOR ARRAY DETAIL · TELEMETRY EVERY 4s
          </p>
          <p className="text-[9px] text-verde-dim">LAST WRITE: {lastUpdate}</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[10px]">
            <thead>
              <tr className="border-b border-verde-border/60 text-verde-muted">
                <th className="px-5 py-2.5 font-normal tracking-widest">CHANNEL</th>
                <th className="px-5 py-2.5 font-normal tracking-widest">LIVE VALUE</th>
                <th className="hidden px-5 py-2.5 font-normal tracking-widest md:table-cell">
                  SENSOR
                </th>
                <th className="hidden px-5 py-2.5 font-normal tracking-widest lg:table-cell">
                  WIRING
                </th>
                <th className="hidden px-5 py-2.5 font-normal tracking-widest sm:table-cell">
                  RANGE
                </th>
              </tr>
            </thead>
            <tbody>
              {SENSOR_ROWS(sensors).map((row) => (
                <tr
                  key={row.name}
                  className="border-b border-verde-border/30 transition-colors last:border-0 hover:bg-verde-green/5"
                >
                  <td className="px-5 py-3 text-verde-text">{row.name}</td>
                  <td className="px-5 py-3 text-verde-green text-glow">
                    {row.value}
                  </td>
                  <td className="hidden px-5 py-3 text-verde-dim md:table-cell">
                    {row.sensor}
                  </td>
                  <td className="hidden px-5 py-3 text-verde-muted lg:table-cell">
                    {row.pin}
                  </td>
                  <td className="hidden px-5 py-3 text-verde-muted sm:table-cell">
                    {row.range}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}
