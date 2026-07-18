// ============================================================
// GET /api/cleanup-storage  (Node.js runtime)
// Vercel cron: nightly. Implements the 15-day TTL policy from
// App/11_Image_Handling.md — deletes any /scans/ file older than
// 15 days so the 5GB free tier never fills up.
// ============================================================
import { NextResponse } from "next/server";
import { adminStorage } from "@/lib/firebaseAdmin";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const TTL_DAYS = 15;

export async function GET(request) {
  try {
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

    const bucket = adminStorage().bucket();
    const [files] = await bucket.getFiles({ prefix: "scans/" });

    const cutoff = Date.now() - TTL_DAYS * 24 * 60 * 60 * 1000;
    let deletedCount = 0;

    for (const file of files) {
      const [metadata] = await file.getMetadata();
      const createdTime = new Date(metadata.timeCreated).getTime();
      if (createdTime < cutoff) {
        await file.delete();
        deletedCount++;
      }
    }

    return NextResponse.json(
      { success: true, scanned: files.length, deleted: deletedCount },
      { status: 200 }
    );
  } catch (error) {
    console.error("cleanup-storage error:", error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
