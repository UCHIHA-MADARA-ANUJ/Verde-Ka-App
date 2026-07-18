# 09. User Authentication & Session Lifecycles

This document outlines the authentication and tokenization strategy for **Project Verde V3.0**.

---

## 🔑 1. Strategy: Firebase Anonymous Authentication

For a competitive live exhibition (DAV ACON 5), the judges will only interact with your app for 2 to 3 minutes. **Asking them to register, type passwords, or verify emails will kill your presentation flow.**

We utilize **Firebase Anonymous Authentication**:
* **How it works:** When the web app loads, it instantly creates a temporary, unique authenticated session in the background without requiring any user input.
* **Security Benefits:** This generates a secure JWT token inside the browser, allowing the client to securely read/write to the Firebase RTDB while fully obeying your strict Database Security Rules.

---

## 🛠️ 2. Step-by-Step Implementation

1. **Install Firebase SDK:**
   `npm install firebase`
2. **Initialize Auth Client:**
```javascript
// lib/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, signInAnonymously } from "firebase/auth";

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  databaseURL: "YOUR_DATABASE_URL",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export const initializeUserSession = async () => {
  try {
    const userCredential = await signInAnonymously(auth);
    console.log("Anonymous UID:", userCredential.user.uid);
    return userCredential.user;
  } catch (error) {
    console.error("Session init failed:", error);
    return null;
  }
};
```

---

## 🔄 3. Token Session Lifecycles
* **Persistence:** The session token is automatically cached in the browser's `IndexedDB` storage by the Firebase Web SDK. If the judge reloads your page, the session is preserved instantly.
* **Revocation:** If the user closes the page, the anonymous session remains valid for 30 days before automatically expiring, ensuring your database remains secure and clutter-free.
