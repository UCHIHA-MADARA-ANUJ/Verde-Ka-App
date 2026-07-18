// ============================================================
// PROJECT VERDE V3.0 — FIREBASE WEB CLIENT (Browser side)
// Lazily initializes the Firebase app, Anonymous Auth and RTDB.
// Lazy init keeps Next.js static prerendering safe (no env vars
// needed at build time) — everything boots on first client call.
// All keys come from NEXT_PUBLIC_* env vars — never hardcoded.
// ============================================================
import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, signInAnonymously, onAuthStateChanged } from "firebase/auth";
import { getDatabase, ref as dbRef } from "firebase/database";

function buildConfig() {
  return {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
    databaseURL: process.env.NEXT_PUBLIC_FIREBASE_DATABASE_URL,
    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
    storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  };
}

export function isFirebaseConfigured() {
  return Boolean(
    process.env.NEXT_PUBLIC_FIREBASE_API_KEY &&
      process.env.NEXT_PUBLIC_FIREBASE_DATABASE_URL
  );
}

/** Singleton Firebase app (created on first use, browser only). */
export function getFirebaseApp() {
  if (!isFirebaseConfigured()) return null;
  return getApps().length ? getApp() : initializeApp(buildConfig());
}

/** Auth instance (or null when unconfigured / during prerender). */
export function getFirebaseAuth() {
  const app = getFirebaseApp();
  return app ? getAuth(app) : null;
}

/** RTDB instance (or null when unconfigured / during prerender). */
export function getRtdb() {
  const app = getFirebaseApp();
  return app ? getDatabase(app) : null;
}

/** Convenience: build a DB ref, returns null if Firebase is not ready. */
export function verdeRef(path) {
  const db = getRtdb();
  return db ? dbRef(db, path) : null;
}

/**
 * Starts a background Anonymous Auth session.
 * Resolves with the Firebase user (or null on failure).
 * Judges never see a login screen — session boots silently.
 */
export function initializeUserSession() {
  return new Promise((resolve) => {
    const auth = getFirebaseAuth();
    if (!auth) {
      console.error("❌ Firebase is not configured (missing env vars).");
      resolve(null);
      return;
    }
    const unsub = onAuthStateChanged(auth, async (user) => {
      unsub();
      if (user) {
        resolve(user);
        return;
      }
      try {
        const cred = await signInAnonymously(auth);
        resolve(cred.user);
      } catch (err) {
        console.error("❌ Anonymous session init failed:", err);
        resolve(null);
      }
    });
  });
}
