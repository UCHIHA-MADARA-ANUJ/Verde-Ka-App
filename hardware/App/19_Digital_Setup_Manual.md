# 19. Anuj's Manual Digital Setup & Prerequisites Guide

This document is the official step-by-step digital configuration manual for **Anuj (Software & Cloud Developer)**. Follow these steps exactly to set up your entire database, storage, local Next.js environment, and API integrations from point zero while Aarav works on the physical hardware wiring.

---

## 📅 THE DIGITAL ARCHITECTURE PIPELINE

```
  [ PHASE 1: FIREBASE ]          [ PHASE 2: NEXT.JS INIT ]        [ PHASE 3: SECURE ENVS ]
  - Create Console Project       - npx create-next-app            - Configure .env.local
  - Setup RTDB (/Garden)         - Install firebase, recharts     - Load API keys securely
  - Setup Storage Bucket         - Configure lib/firebase.js
  - Enable Anonymous Auth
           │                                │                                │
           ▼                                ▼                                ▼
  [ PHASE 4: API SOURCING ]      [ PHASE 5: SERVERLESS APIS ]     [ PHASE 6: DASHBOARD UI ]
  - OpenWeatherMap (Weather)     - /api/upload-photo (Node)       - Renders live G-V-S data
  - Plant.id (Diagnosis)         - /api/analyze-plant (Edge)      - Recharts moisture plots
  - Gemini 2.0 (AI Chatbot)      - /api/weather-sync (Edge)       - Dynamic AI chatbot terminal
```

---

## 🛠️ PHASE 1: FIREBASE PROJECT CONFIGURATION (CLOUD CORE)

Follow these steps exactly in your web browser to initialize the cloud database and asset buckets:

### Step 1.1: Create Your Firebase Project
1. Open your browser and go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **"Add Project"**.
3. Name your project: **`Project-Verde-V3`** (or your own custom name).
4. **Google Analytics:** Disable Google Analytics for this project (keeps the setup faster and avoids unnecessary tracker scripts during the exhibition).
5. Click **"Create Project"** and wait for the workspace to initialize.

### Step 1.2: Set Up the Realtime Database (RTDB)
1. On the left-hand sidebar of your project dashboard, click **"Build"** -> select **"Realtime Database"**.
2. Click **"Create Database"**.
3. **Database Location:** Select **"Singapore (asia-southeast1)"** (recommended for lowest latency in India/Delhi NCR) or **"United States (us-central1)"**.
4. **Security Rules:** Select **"Start in Test Mode"** (this sets `.read` and `.write` to `true` temporarily so you can test, but we will upgrade these rules in Phase 1.5).
5. Click **"Enable"**. Your live database URL (e.g. `https://your-project-id-default-rtdb.firebaseio.com/`) is now active. **Copy this URL!**

### Step 1.3: Set Up Cloud Storage
1. On the left sidebar, click **"Build"** -> select **"Storage"**.
2. Click **"Get Started"**.
3. **Security Rules:** Select **"Start in Test Mode"** and click **"Next"**.
4. **Storage Location:** Keep the default Google Cloud Storage bucket region (e.g. `us.artifacts...` or `asia-east1`) and click **"Done"**.
5. Wait for the storage bucket to compile. Your secure bucket link (e.g. `gs://your-project-id.appspot.com`) is now live. **Copy this link!**

### Step 1.4: Enable Anonymous Authentication
1. On the left sidebar, click **"Build"** -> select **"Authentication"**.
2. Click **"Get Started"**.
3. Go to the **"Sign-in Method"** tab.
4. Under the "Other providers" list, click on **"Anonymous"**.
5. Toggle the switch to **"Enable"** and click **"Save"**.
* *Why:* This allows your Next.js frontend to securely log judges in in-background with zero loading delays, granting them encrypted tokens to read/write without typing emails or passwords!

### Step 1.5: Apply Production Security Rules
Go back to your **Realtime Database** tab, click **"Rules"**, and replace the JSON tree with this exact schema to secure your water pump and grow lights while keeping the connection open for your ESP32 boards:

```json
{
  "rules": {
    "Garden": {
      // Only authenticated anonymous users or your ESP32 secret key can read/write!
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```
*Click **"Publish"** to save.*

Next, go to your **Storage** tab, click **"Rules"**, and replace the storage rules with this schema so your ESP32-CAM uploaded leaf photos can render publicly but can only be uploaded by secure authenticated routes:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      allow read: if true; // Publicly readable for dashboard rendering
      allow write: if request.auth != null; // Only authenticated APIs can write
    }
  }
}
```
*Click **"Publish"** to save.*

---

## 💻 PHASE 2: NEXT.JS ENVIRONMENT INITIALIZATION (LOCAL DEV)

Open your terminal on your local laptop (Lenovo Legion 7) and run these commands:

### Step 2.1: Bootstrap Next.js
Initialize your application structure using the modern Next.js App Router:
```bash
npx create-next-app@latest next-app --js --tailwind --eslint --app
```
*Configure options when prompted:*
* *Would you like to use TypeScript?* **No** (keeps prototyping simple and fast)
* *Would you like to use Src directory?* **No**
* *Would you like to use Turbopack?* **Yes**
* *Would you like to customize default import alias?* **No**

### Step 2.2: Install Core Dependencies
Navigate into your new directory and install the necessary real-time sync, charting, and motion libraries:
```bash
cd next-app
npm install firebase recharts framer-motion lucide-react
```

---

## 🔑 PHASE 3: SECURE ENVIRONMENT VARIABLES (`.env.local`)

To prevent exposing database secrets or API keys on your public GitHub repository, create a secure local environment file.

1. In the root of your `next-app/` folder, create a new file named **`.env.local`**.
2. Paste this exact structure, replacing the placeholders with your actual credentials:

```text
# === FIREBASE CLIENT SECRETS ===
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_DATABASE_URL=https://your_project_id-default-rtdb.firebaseio.com/
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com

# === PRIVATE BACKEND API KEYS ===
CAM_UPLOAD_API_KEY=your_secure_random_string_for_cam_verification
OPENWEATHER_API_KEY=your_openweathermap_api_key_token
PLANT_ID_API_KEY=your_plant_id_developer_api_key
GEMINI_API_KEY=your_google_studio_gemini_api_key
```

---

## 📡 PHASE 4: THIRD-PARTY API REGISTRATION

You need to register and obtain free developer API keys from three services. These keys must be pasted into your `.env.local` file immediately:

### A. OpenWeatherMap API Key (For Rain Suspend)
1. Go to [OpenWeatherMap](https://openweathermap.org/api) and sign up for a free account.
2. Under your profile, click **"My API Keys"**.
3. Generate a free key and copy it into `OPENWEATHER_API_KEY`.
* *Parameters to use in code:* Delhi coordinates: **`LAT: 28.6139`**, **`LON: 77.209`**.

### B. Plant.id API Key (For Leaf Diagnostics)
1. Go to [Plant.id](https://www.plant.id/) (by FlowerChecker) and sign up for a developer account.
2. Go to the developer console, copy your free trial API key, and paste it into `PLANT_ID_API_KEY`. This provides up to 100 free plant leaf scans per month!

### C. Google Gemini API Key (For Conversational Bot)
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Log in with your standard Google Account.
3. Click **"Get API Key"** -> **"Create API Key in New Project"**.
4. Copy the generated key and paste it into `GEMINI_API_KEY`. This runs the ultra-fast, high-capability **Gemini 2.0 Flash** model completely free under their developer tier!

---

## 🔌 PHASE 5: INITIALIZE FIREBASE WEB CLIENT

Inside your Next.js directory, create your Firebase WebSocket client connector:

1. Create a folder named **`lib`** under your root directory.
2. Inside `lib/`, create a file named **`firebase.js`** and paste this code:

```javascript
// lib/firebase.js
import { initializeApp, getApps, getApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";
import { getAuth, signInAnonymously } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.NEXT_PUBLIC_FIREBASE_DATABASE_URL,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
};

// Prevent duplicate initialization during hot-reloads in local development
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
const db = getDatabase(app);
const storage = getStorage(app);
const auth = getAuth(app);

// Automated Anonymous Sign-In on mount
export const connectUserSession = async () => {
  try {
    if (!auth.currentUser) {
      const userCredential = await signInAnonymously(auth);
      console.log("Secure Anonymous Session active! UID:", userCredential.user.uid);
      return userCredential.user;
    }
    return auth.currentUser;
  } catch (error) {
    console.error("Firebase Auth session failed:", error);
    return null;
  }
};

export { db, storage, auth };
```
