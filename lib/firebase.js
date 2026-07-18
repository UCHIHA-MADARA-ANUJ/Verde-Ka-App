// ============================================================
// PROJECT VERDE V3.0 — FIREBASE WEB CLIENT (Browser side)
// Priority: env vars (Vercel) → committed lib/firebaseConfig.js.
// Lazy init keeps Next.js static prerendering safe.
// ============================================================
import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, signInAnonymously, onAuthStateChanged } from "firebase/auth";
import { getDatabase, ref as dbRef } from "firebase/database";
import { FIREBASE_CLIENT_CONFIG } from "@/lib/firebaseConfig";

function buildConfig() {
  const env = {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
    databaseURL: process.env.NEXT_PUBLIC_FIREBASE_DATABASE_URL,
    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
    storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  };
  if (env.apiKey && env.databaseURL) return env;
  return FIREBASE_CLIENT_CONFIG;
}

export function isFirebaseConfigured() {
  const c = buildConfig();
  return Boolean(
    c.apiKey && c.databaseURL && !String(c.apiKey).startsWith("PASTE_")
  );
}

export function getFirebaseApp() {
  if (!isFirebaseConfigured()) return null;
  return getApps().length ? getApp() : initializeApp(buildConfig());
}

export function getFirebaseAuth() {
  const app = getFirebaseApp();
  return app ? getAuth(app) : null;
}

export function getRtdb() {
  const app = getFirebaseApp();
  return app ? getDatabase(app) : null;
}

export function verdeRef(path) {
  const db = getRtdb();
  return db ? dbRef(db, path) : null;
}

export function initializeUserSession() {
  return new Promise((resolve) => {
    const auth = getFirebaseAuth();
    if (!auth) {
      console.error("❌ Firebase is not configured.");
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
