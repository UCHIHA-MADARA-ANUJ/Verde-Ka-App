// ============================================================
// VERDE FIREBASE CLIENT CONFIG
// These are the PUBLIC web-client keys (they ship to every
// browser anyway — safe to commit). Server secrets (admin key,
// Gemini, Plant.id, OWM) must ONLY live in Vercel env vars!
//
// >>> PASTE YOUR VALUES FROM Firebase Console → Project Settings
// >>> → Your apps → Web app → firebaseConfig
// ============================================================
export const FIREBASE_CLIENT_CONFIG = {
  apiKey: "PASTE_API_KEY",
  authDomain: "PASTE_AUTH_DOMAIN",
  databaseURL: "PASTE_DATABASE_URL",
  projectId: "PASTE_PROJECT_ID",
  storageBucket: "PASTE_STORAGE_BUCKET",
  messagingSenderId: "PASTE_SENDER_ID",
  appId: "PASTE_APP_ID",
};
