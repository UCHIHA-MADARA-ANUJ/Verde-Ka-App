// ============================================================
// POST /api/analyze-plant  (Edge runtime — low latency)
// 1. Receives { imageUrl } OR { imageDataUrl } (base64 Plan B mode).
// 2. Calls Plant.id to identify species + disease probabilities.
// 3. Feeds the structured diagnosis into Gemini 2.0 Flash for a
//    friendly, step-by-step organic treatment plan.
// 4. Returns { plant_identified, health_diagnosis, gemini_remedy }.
// ============================================================
import { NextResponse } from "next/server";

export const runtime = "edge";
export const dynamic = "force-dynamic";

async function fetchImageAsBase64(imageUrl) {
  const res = await fetch(imageUrl);
  if (!res.ok) throw new Error(`Image fetch failed (${res.status})`);
  const buf = await res.arrayBuffer();
  // Chunked base64 conversion (Edge-safe, avoids call stack overflow)
  const bytes = new Uint8Array(buf);
  let binary = "";
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK) {
    binary += String.fromCharCode(...bytes.subarray(i, i + CHUNK));
  }
  return btoa(binary);
}

async function identifyWithPlantId(base64Image) {
  const res = await fetch("https://api.plant.id/v2/identify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Api-Key": process.env.PLANT_ID_API_KEY,
    },
    body: JSON.stringify({
      images: [base64Image],
      modifiers: ["crops_fast", "similar_images"],
      plant_details: ["common_names", "url", "wiki_description"],
      disease_details: ["description", "treatment"],
    }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Plant.id error ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

function summarizeDiagnosis(plantIdJson) {
  const suggestion = plantIdJson?.suggestions?.[0];
  const plantName = suggestion
    ? `${suggestion.plant_name}${
        suggestion.plant_details?.common_names?.length
          ? ` (${suggestion.plant_details.common_names[0]})`
          : ""
      }`
    : "Unknown plant";
  const probability = suggestion
    ? Math.round((suggestion.probability || 0) * 100)
    : 0;

  const disease = plantIdJson?.health_assessment?.diseases?.[0];
  const diseaseText = disease
    ? `${disease.name} (${Math.round((disease.probability || 0) * 100)}% confidence)`
    : "No visible disease detected";

  return { plantName, probability, diseaseText };
}

async function remedyWithGemini({ plantName, diseaseText }) {
  const prompt =
    `You are Verde AI, a botanical specialist embedded in a smart-garden ` +
    `monitoring terminal. The user's plant photo has been identified as ` +
    `"${plantName}" and diagnosed with: ${diseaseText}. ` +
    `Formulate a friendly, step-by-step organic treatment plan in under ` +
    `160 words. Prefer neem-oil, watering-schedule and light adjustments. ` +
    `Format as short numbered steps suitable for a monospace terminal.`;

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
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
    throw new Error(`Gemini error ${res.status}: ${text.slice(0, 200)}`);
  }
  const json = await res.json();
  return (
    json?.candidates?.[0]?.content?.parts?.[0]?.text?.trim() ||
    "Diagnosis complete. Maintain the current care routine and re-scan in 3 days."
  );
}

export async function POST(request) {
  try {
    const { imageUrl, imageDataUrl } = await request.json();

    let base64;
    if (imageDataUrl && imageDataUrl.startsWith("data:image/jpeg;base64,")) {
      // Plan B: base64 payload came straight from RTDB — no fetch needed
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

    const plantIdJson = await identifyWithPlantId(base64);
    const { plantName, probability, diseaseText } =
      summarizeDiagnosis(plantIdJson);
    const remedy = await remedyWithGemini({ plantName, diseaseText });

    return NextResponse.json(
      {
        success: true,
        plant_identified: plantName,
        identification_confidence: probability,
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
