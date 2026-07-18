# 11. Image Handling & Storage Lifecycle

This document outlines the end-to-end binary buffer upload, compression, and automated cleanup (TTL) pipeline of plant leaf photographs.

---

## 📦 1. The Image Upload Pipeline

```
[ ESP32-CAM ]               [ Next.js API ]               [ Firebase Storage ]
      │                            │                               │
      │──(1. POSTs raw JPEG)──────►│                               │
      │   Buffer in RAM            │                               │
      │                            │──(2. Streams binary buffer)──►│
      │                            │   File: current_capture.jpg   │
      │◄──(3. Returns 200 OK)──────┼───────────────────────────────│
```

### Steps:
1. **On-Demand Snap:** ESP32-CAM captures a JPEG frame at `SVGA (800x600)` with `jpeg_quality = 10` to keep the file size very small (~60 KB), preventing Wi-Fi packet drops.
2. **Buffer Stream:** The camera posts the raw binary JPEG bytes directly to the `/api/upload-photo` Vercel route over WiFi.
3. **Storage Save:** The Next.js API receives the binary buffer and streams it straight to Firebase Storage under the folder: `/scans/{userId}/current_capture.jpg`.

---

## 🗑️ 2. The 15-Day Auto-Delete Lifecycle Policy (TTL)

To prevent your 5GB free storage tier from filling up, you must implement an automated **Time-To-Live (TTL)** cleanup routine. We write a serverless Vercel cron route that runs once every night:

```javascript
// app/api/cleanup-storage/route.js
import { getStorage } from "firebase-admin/storage";
import { NextResponse } from "next/server";

export async function GET(request) {
  try {
    const bucket = getStorage().bucket();
    const [files] = await bucket.getFiles({ prefix: "scans/" });
    
    const fifteenDaysAgo = Date.now() - (15 * 24 * 60 * 60 * 1000);
    let deletedCount = 0;
    
    for (const file of files) {
      const [metadata] = await file.getMetadata();
      const createdTime = new Date(metadata.timeCreated).getTime();
      
      if (createdTime < fifteenDaysAgo) {
        await file.delete();
        deletedCount++;
      }
    }
    
    return NextResponse.json({ success: true, deleted: deletedCount });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
```
* **Benefit:** This keeps your storage footprint incredibly low, meaning your 5GB free tier will **never run out of space**!
