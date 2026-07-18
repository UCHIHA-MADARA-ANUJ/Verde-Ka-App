// ============================================================
// Landing splash page — terminal boot screen aesthetic.
// Routes the user into /dashboard.
// ============================================================
import Link from "next/link";

const BOOT_LINES = [
  "[ OK ] mounting sensor bus........... DHT22 / HC-SR04 / LDR / SOIL",
  "[ OK ] actuator rail check........... PUMP_RELAY(25) UV_LED(26)",
  "[ OK ] vision node handshake......... ESP32-CAM @ 8MHz XCLK",
  "[ OK ] cloud bridge.................. FIREBASE RTDB <100ms",
  "[ OK ] ai stack...................... PLANT.ID + GEMINI 2.0 FLASH",
];

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6">
      <div className="crt relative w-full max-w-2xl rounded-lg border border-verde-border bg-verde-panel p-8 shadow-glow">
        <p className="mb-1 text-xs text-verde-muted">
          VERDE TECH // AUTONOMOUS PLANT OS
        </p>
        <h1 className="mb-6 text-3xl text-verde-green text-glow sm:text-4xl">
          PROJECT VERDE <span className="text-verde-text">V3.0</span>
        </h1>

        <div className="mb-8 space-y-1.5 text-[11px] leading-relaxed text-verde-dim sm:text-xs">
          {BOOT_LINES.map((line) => (
            <p key={line}>{line}</p>
          ))}
          <p className="text-verde-green">
            [ OK ] system nominal. awaiting operator
            <span className="animate-blink">▌</span>
          </p>
        </div>

        <Link
          href="/dashboard"
          className="inline-block rounded border border-verde-green bg-verde-green/10 px-6 py-3 text-sm text-verde-green transition-all duration-200 hover:bg-verde-green/20 hover:shadow-glow"
        >
          ▶ ENTER CONTROL DECK
        </Link>

        <p className="mt-6 text-[10px] text-verde-muted">
          DAV ACON 5 TECH EXHIBITION · ESP32 WROOM-32 + ESP32-CAM ·
          FIREBASE RTDB · DELHI, IN
        </p>
      </div>
    </main>
  );
}
