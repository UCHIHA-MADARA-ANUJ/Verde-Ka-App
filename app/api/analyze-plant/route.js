// ============================================================
// POST /api/analyze-plant  (Edge runtime — low latency)
// 1. Receives { imageUrl } OR { imageDataUrl } (base64 RTDB mode).
// 2. Calls Kindwise crop.health API to identify the crop and
//    score disease probabilities (works with CROP_HEALTH_API_KEY).
// 3. Feeds the diagnosis into Gemini 2.0 Flash for a friendly,
//    step-by-step organic treatment plan.
// 4. Returns { plant_identified, health_diagnosis, gemini_remedy }.
// ============================================================
import { NextResponse } from "next/server";

export const runtime = "edge";
export const dynamic = "force-dynamic";

async function fetchImageAsBase64(imageUrl) {
  const res = await fetch(imageUrl);
  if (!res.ok) throw new Error(`Image fetch failed (${res.status})`);
  const buf = await res.arrayBuffer();
  const bytes = new Uint8Array(buf);
  let binary = "";
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK) {
    binary += String.fromCharCode(...bytes.subarray(i, i + CHUNK));
  }
  return btoa(binary);
}

// ---- Kindwise crop.health identification ----
async function identifyWithCropHealth(base64Image) {
  const apiKey =
    process.env.CROP_HEALTH_API_KEY || process.env.PLANT_ID_API_KEY;
  const res = await fetch(
    "https://crop.kindwise.com/api/v1/identification",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Api-Key": apiKey,
      },
      body: JSON.stringify({
        images: [`data:image/jpeg;base64,${base64Image}`],
        similar_images: false,
      }),
    }
  );
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`crop.health error ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

function summarizeDiagnosis(json) {
  const crop = json?.result?.crop?.suggestions?.[0];
  const plantName = crop
    ? `${crop.name}${
        crop.scientific_name && crop.scientific_name !== crop.name
          ? ` (${crop.scientific_name})`
          : ""
      }`
    : "Unknown plant";

  const disease = json?.result?.disease?.suggestions?.[0];
  const diseaseText = disease
    ? `${disease.name} (${Math.round((disease.probability || 0) * 100)}% confidence)`
    : "No visible disease detected";

  return { plantName, diseaseText };
}

// Model fallback chain — live-tested against this key on 2026-07-18:
// gemini-2.5-flash ✅ · flash-lite ✅ · flash-latest ✅ (2.0-flash was 429)
const GEMINI_MODELS = [
  "gemini-2.5-flash",
  "gemini-2.5-flash-lite",
  "gemini-flash-latest",
];

async function remedyWithGemini({ plantName, diseaseText }) {
  const prompt =
    `You are Verde AI, a botanical specialist embedded in a smart-garden ` +
    `monitoring terminal. The user's plant photo has been identified as ` +
    `"${plantName}" and diagnosed with: ${diseaseText}. ` +
    `Formulate a friendly, step-by-step organic treatment plan in under ` +
    `160 words. Prefer neem-oil, watering-schedule and light adjustments. ` +
    `Format as short numbered steps suitable for a monospace terminal.`;

  let lastErr = null;
  for (const model of GEMINI_MODELS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${process.env.GEMINI_API_KEY}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { temperature: 0.6, maxOutputTokens: 512 },
          }),
        }
      );
      if (!res.ok) {
        const text = await res.text();
        lastErr = new Error(
          `Gemini ${model} error ${res.status}: ${text.slice(0, 150)}`
        );
        continue; // quota/availability issue → try next model
      }
      const json = await res.json();
      const out = json?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
      if (out) return out;
      lastErr = new Error(`Gemini ${model} returned empty response`);
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr || new Error("All Gemini models failed");
}

export async function POST(request) {
  try {
    const { imageUrl, imageDataUrl } = await request.json();

    let base64;
    if (imageDataUrl && imageDataUrl.startsWith("data:image/jpeg;base64,")) {
      base64 = imageDataUrl.slice("data:image/jpeg;base64,".length);
    } else if (imageUrl && /^https:\/\//.test(imageUrl)) {
      base64 = await fetchImageAsBase64(imageUrl);
    } else {
      return NextResponse.json(
        {
          success: false,
          error: "A valid https imageUrl or a jpeg imageDataUrl is required",
        },
        { status: 400 }
      );
    }

    const cropJson = await identifyWithCropHealth(base64);
    const { plantName, diseaseText } = summarizeDiagnosis(cropJson);

    let remedy;
    try {
      remedy = await remedyWithGemini({ plantName, diseaseText });
    } catch (gemErr) {
      // Gemini failure should not kill the whole diagnosis
      console.error("Gemini fallback:", gemErr.message);
      remedy =
        `Diagnosis: ${diseaseText}. ` +
        `General guidance: remove badly affected leaves, spray diluted ` +
        `neem-oil weekly at dusk, avoid overhead watering, and re-scan in 3 days.`;
    }

    return NextResponse.json(
      {
        success: true,
        plant_identified: plantName,
        health_diagnosis: diseaseText,
        gemini_remedy: remedy,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("analyze-plant error:", error);
    return NextResponse.json(
      { success: false, error: error.message || "Analysis failed" },
      { status: 500 }
    );
  }
}
