// ============================================================
// POST /api/upload-photo  (Node.js runtime — binary buffer handling)
// Receives raw JPEG bytes from the ESP32-CAM, validates x-api-key,
// then stores the photo using a two-tier strategy:
//
//   TIER 1 (preferred): stream buffer to Firebase Storage /scans/
//   TIER 2 (Plan B):    if Storage fails (no Blaze plan, bucket
//                       missing, any error) OR PHOTO_STORAGE_MODE=rtdb,
//                       store the JPEG as a base64 data-URL directly
//                       inside RTDB /latest_scan (SVGA ~60KB → ~80KB,
//                       perfectly fine for the exhibition demo).
//
// Either way: resets capture_photo and records /latest_scan.
// ============================================================
import { NextResponse } from "next/server";
import { adminStorage, adminDatabase } from "@/lib/firebaseAdmin";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const MAX_BYTES = 2 * 1024 * 1024; // 2 MB hard cap (SVGA ~60KB typical)
// RTDB values are capped well above this, but keep base64 payloads sane:
const MAX_RTDB_BYTES = 400 * 1024; // 400 KB raw → ~533 KB base64

async function saveToStorage(buffer, stamp) {
  const bucket = adminStorage().bucket();
  const filePath = `scans/verde-node-1/capture_${stamp}.jpg`;
  const file = bucket.file(filePath);

  await file.save(buffer, {
    metadata: {
      contentType: "image/jpeg",
      cacheControl: "public, max-age=60",
    },
    resumable: false,
  });
  await file.makePublic();

  return `https://storage.googleapis.com/${bucket.name}/${filePath}`;
}

export async function POST(request) {
  try {
    // --- 1. API key guard (prevents storage spamming) ---
    const apiKey = request.headers.get("x-api-key");
    if (
      !process.env.CAM_UPLOAD_API_KEY ||
      apiKey !== process.env.CAM_UPLOAD_API_KEY
    ) {
      return NextResponse.json(
        { success: false, error: "Invalid API Key header" },
        { status: 401 }
      );
    }

    // --- 2. Read the raw binary body ---
    const arrayBuffer = await request.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    if (!buffer.length) {
      return NextResponse.json(
        { success: false, error: "Empty image payload" },
        { status: 400 }
      );
    }
    if (buffer.length > MAX_BYTES) {
      return NextResponse.json(
        { success: false, error: "Payload too large" },
        { status: 413 }
      );
    }
    // JPEG magic bytes sanity check (FF D8)
    if (buffer[0] !== 0xff || buffer[1] !== 0xd8) {
      return NextResponse.json(
        { success: false, error: "Payload is not a valid JPEG" },
        { status: 415 }
      );
    }

    const stamp = Date.now();
    const db = adminDatabase();

    // --- 3. TIER 1: Firebase Storage (unless forced to rtdb mode) ---
    let imageUrl = null;
    let storageMode = "storage";
    let storageError = null;

    if (process.env.PHOTO_STORAGE_MODE !== "rtdb") {
      try {
        imageUrl = await saveToStorage(buffer, stamp);
      } catch (err) {
        storageError = err.message;
        console.warn(
          "Storage tier failed, falling back to RTDB base64:",
          err.message
        );
      }
    }

    // --- 4. TIER 2 (Plan B): base64 data-URL inside RTDB ---
    let imageDataUrl = null;
    if (!imageUrl) {
      storageMode = "rtdb-base64";
      if (buffer.length > MAX_RTDB_BYTES) {
        return NextResponse.json(
          {
            success: false,
            error: `Storage unavailable (${storageError}) and image too large for RTDB fallback (${buffer.length} bytes > ${MAX_RTDB_BYTES}). Lower jpeg_quality / frame size on the CAM.`,
          },
          { status: 507 }
        );
      }
      imageDataUrl = `data:image/jpeg;base64,${buffer.toString("base64")}`;
    }

    // --- 5. Release the app spinner + record the scan ---
    await Promise.all([
      db.ref("/controls/capture_photo").set(false),
      db.ref("/latest_scan").set({
        imageUrl: imageUrl || null,
        imageDataUrl: imageDataUrl || null,
        captured_at: stamp,
        status: "uploaded",
        storage_mode: storageMode,
        diagnosis: null,
      }),
    ]);

    return NextResponse.json(
      {
        success: true,
        storage_mode: storageMode,
        imageUrl: imageUrl || undefined,
        bytes: buffer.length,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("upload-photo error:", error);
    // Best effort: still release the dashboard spinner on hard failure
    try {
      await adminDatabase().ref("/controls/capture_photo").set(false);
    } catch {}
    return NextResponse.json(
      { success: false, error: error.message || "Upload failed" },
      { status: 500 }
    );
  }
}
