// ============================================================
// GET /api/weather-sync  (Node runtime for Admin SDK writes)
// Vercel cron: every hour. Fetches Delhi weather from
// OpenWeatherMap. If rain/drizzle/thunderstorm is detected,
// writes weather_override = 1 into /controls, else 0.
// The ESP32 reads this flag and suspends irrigation before rain.
// ============================================================
import { NextResponse } from "next/server";
import { adminDatabase } from "@/lib/firebaseAdmin";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const DELHI = { lat: 28.6139, lon: 77.209 };
const RAIN_CONDITIONS = ["rain", "drizzle", "thunderstorm"];

export async function GET(request) {
  try {
    // Optional cron guard: Vercel sends Authorization: Bearer CRON_SECRET
    const authHeader = request.headers.get("authorization");
    if (
      process.env.CRON_SECRET &&
      authHeader !== `Bearer ${process.env.CRON_SECRET}`
    ) {
      return NextResponse.json(
        { success: false, error: "Unauthorized" },
        { status: 401 }
      );
    }

    const url =
      `https://api.openweathermap.org/data/2.5/weather` +
      `?lat=${DELHI.lat}&lon=${DELHI.lon}` +
      `&appid=${process.env.OPENWEATHER_API_KEY}&units=metric`;

    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`OpenWeatherMap error ${res.status}`);
    }
    const data = await res.json();

    const mainCondition = (data?.weather?.[0]?.main || "Clear").toLowerCase();
    const description = data?.weather?.[0]?.description || "clear sky";
    const temp = data?.main?.temp ?? null;
    const isRainy = RAIN_CONDITIONS.some((c) => mainCondition.includes(c));
    const override = isRainy ? 1 : 0;

    const db = adminDatabase();
    await Promise.all([
      db.ref("/controls/weather_override").set(override),
      db.ref("/weather").update({
        condition: data?.weather?.[0]?.main || "Clear",
        description,
        temp,
        city: "Delhi",
        synced_at: Date.now(),
      }),
    ]);

    return NextResponse.json(
      {
        success: true,
        weather: data?.weather?.[0]?.main || "Clear",
        description,
        override_written: override,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("weather-sync error:", error);
    return NextResponse.json(
      { success: false, error: error.message || "Weather sync failed" },
      { status: 500 }
    );
  }
}
