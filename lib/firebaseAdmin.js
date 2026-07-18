// ============================================================
// PROJECT VERDE V3.0 — FIREBASE ADMIN SDK (Server side ONLY)
// Used by Node.js API routes: photo upload, storage cleanup,
// weather override writes. Credentials come from server env vars.
// ============================================================
import { initializeApp, getApps, cert } from "firebase-admin/app";
import { getStorage } from "firebase-admin/storage";
import { getDatabase } from "firebase-admin/database";

function getAdminApp() {
  if (getApps().length) return getApps()[0];

  const privateKey = (process.env.FIREBASE_PRIVATE_KEY || "").replace(
    /\\n/g,
    "\n"
  );

  return initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey,
    }),
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    databaseURL: process.env.FIREBASE_DATABASE_URL,
  });
}

export function adminStorage() {
  return getStorage(getAdminApp());
}

export function adminDatabase() {
  return getDatabase(getAdminApp());
}
