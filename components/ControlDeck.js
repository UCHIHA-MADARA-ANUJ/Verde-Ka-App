"use client";
// Manual Override Panel — mode toggle, threshold slider, actuators.
// Every write lands in /controls and reaches the ESP32 in <100ms.
import { motion } from "framer-motion";
import { Power, Droplet, Lightbulb, CloudRain, Bot, Hand } from "lucide-react";

function Row({ children }) {
  return (
    <div className="flex items-center justify-between border-b border-verde-border/60 py-3 last:border-0">
      {children}
    </div>
  );
}

function Toggle({ on, onClick, disabled, activeColor = "#22c55e" }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`relative h-6 w-12 rounded-full border transition-all duration-200 ${
        disabled
          ? "cursor-not-allowed border-verde-border opacity-40"
          : on
          ? "border-transparent"
          : "border-verde-border bg-verde-panel"
      }`}
      style={
        on && !disabled
          ? { background: activeColor, boxShadow: `0 0 12px ${activeColor}66` }
          : {}
      }
    >
      <motion.span
        layout
        transition={{ type: "spring", stiffness: 500, damping: 32 }}
        className={`absolute top-0.5 h-4.5 w-4.5 rounded-full ${
          on ? "right-0.5 bg-verde-bg" : "left-0.5 bg-verde-muted"
        }`}
        style={{ width: 18, height: 18 }}
      />
    </button>
  );
}

export default function ControlDeck({ controls, setControl, online, tankLevel }) {
  const manual = !!controls.manual_mode;
  const frozen = !online; // freeze switches when edge is offline (doc 12)
  const tankEmpty = (tankLevel ?? 0) < 10;

  return (
    <div className="crt relative flex flex-col rounded-lg border border-verde-border bg-verde-card p-5 transition-shadow hover:shadow-glow">
      <p className="mb-2 text-[10px] tracking-widest text-verde-muted">
        ▓ MANUAL OVERRIDE DECK
      </p>

      {frozen && (
        <p className="mb-2 rounded border border-verde-danger/40 bg-red-950/20 px-2 py-1.5 text-[10px] text-verde-danger">
          ⚠ EDGE OFFLINE — controls frozen. Device is running autonomously.
        </p>
      )}

      {/* Mode toggle */}
      <Row>
        <span className="flex items-center gap-2 text-xs text-verde-text">
          {manual ? <Hand size={14} /> : <Bot size={14} />}
          MODE: {manual ? "MANUAL" : "AUTONOMOUS"}
        </span>
        <Toggle
          on={manual}
          disabled={frozen}
          onClick={() => setControl({ manual_mode: !manual })}
        />
      </Row>

      {/* Threshold slider */}
      <div className="border-b border-verde-border/60 py-3">
        <div className="mb-2 flex items-center justify-between text-xs">
          <span className="text-verde-text">SOIL MOISTURE TARGET</span>
          <span className="text-verde-green text-glow">
            {controls.moisture_threshold}%
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={100}
          step={1}
          disabled={frozen}
          value={controls.moisture_threshold}
          onChange={(e) =>
            setControl({ moisture_threshold: Number(e.target.value) })
          }
          className="verde-slider"
          style={{ "--fill": `${controls.moisture_threshold}%` }}
        />
      </div>

      {/* Pump */}
      <Row>
        <span className="flex items-center gap-2 text-xs text-verde-text">
          <Droplet size={14} className={controls.pump_state ? "text-verde-water" : ""} />
          WATER PUMP
          {controls.pump_state && (
            <span className="text-[9px] text-verde-water">● RUNNING</span>
          )}
        </span>
        <Toggle
          on={!!controls.pump_state}
          activeColor="#38bdf8"
          disabled={frozen || !manual || tankEmpty}
          onClick={() => setControl({ pump_state: !controls.pump_state })}
        />
      </Row>
      {tankEmpty && (
        <p className="pb-2 text-[9px] text-verde-danger">
          ⛔ DRY-RUN LOCKOUT: reservoir &lt;10% — pump trigger disabled.
        </p>
      )}

      {/* Grow light */}
      <Row>
        <span className="flex items-center gap-2 text-xs text-verde-text">
          <Lightbulb
            size={14}
            className={controls.grow_light_state ? "text-purple-400" : ""}
          />
          UV GROW LIGHT
          {controls.grow_light_state && (
            <span className="text-[9px] text-purple-400">● 395nm ACTIVE</span>
          )}
        </span>
        <Toggle
          on={!!controls.grow_light_state}
          activeColor="#a855f7"
          disabled={frozen || !manual}
          onClick={() =>
            setControl({ grow_light_state: !controls.grow_light_state })
          }
        />
      </Row>

      {!manual && (
        <p className="pt-2 text-[9px] text-verde-muted">
          <Power size={9} className="mr-1 inline" />
          Actuator toggles unlock in MANUAL mode. Autonomous botanist is in
          command.
        </p>
      )}

      {/* Weather override banner */}
      {controls.weather_override === 1 && (
        <div className="mt-3 flex items-center gap-2 rounded border border-verde-water/50 bg-sky-950/30 px-3 py-2 text-[10px] text-verde-water shadow-glow-water">
          <CloudRain size={13} />
          RAIN PREDICTED IN DELHI — AUTOMATED IRRIGATION SUSPENDED
        </div>
      )}
    </div>
  );
}
