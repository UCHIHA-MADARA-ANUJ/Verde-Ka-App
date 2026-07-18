# 🌱 VERDE TECH V3.0 — THE COMPLETE SETUP BIBLE
### Every click, every key, every rule — from zero to live production system

Follow this top-to-bottom. Total time: ~45 minutes. You need: a Google account,
a GitHub account, and the two ESP32 boards.

---

# PART 1 — FIREBASE PROJECT (the cloud brain)

## Step 1.1 — Create the project
1. Go to **https://console.firebase.google.com**
2. Click **"Create a Firebase project"** (or "Add project").
3. Project name: `verde-tech-v3` → Continue.
4. Google Analytics: **Disable** (not needed, keeps it simple) → **Create project**.
5. Wait ~30s → **Continue**.

## Step 1.2 — Create the Realtime Database (RTDB)
1. Left sidebar → **Build → Realtime Database** → **Create Database**.
2. Location: **Singapore (asia-southeast1)** — closest region to Delhi. ⚠️ Cannot be changed later!
3. Security rules: pick **"Start in locked mode"** (we paste our own rules next) → **Enable**.
4. 📋 **COPY YOUR DATABASE URL** shown at the top, e.g.:
   `https://verde-tech-v3-default-rtdb.asia-southeast1.firebasedatabase.app`
   You will need this in 4 places later.

## Step 1.3 — Paste the Database Rules
1. In Realtime Database → click the **"Rules"** tab.
2. Delete everything there and paste this (from `firebase/database.rules.json`):

```json
{
  "rules": {
    ".read": false,
    ".write": false,
    "sensors": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "controls": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "historical_logs": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "latest_scan": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "weather": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```
3. Click **"Publish"**. ✅ Your DB is now locked to authenticated sessions only.

## Step 1.4 — Seed the database tree (initial values)
1. Click the **"Data"** tab.
2. Click the **⋮ (three dots)** menu → **"Import JSON"**.
3. Upload the file **`firebase/seed.json`** from this project.
   (Or manually create the nodes — the import is instant and error-free.)
4. You should now see `sensors`, `controls`, `historical_logs`, `latest_scan`,
   `weather` in the tree. ✅

## Step 1.5 — Enable Cloud Storage
1. Sidebar → **Build → Storage** → **Get started**.
2. Keep the default bucket → **"Start in production mode"** → Done.
   > ⚠️ If Firebase asks you to upgrade to the Blaze plan for Storage: Blaze is
   > still **free within the free quotas** (5GB) but needs a card on file. If
   > you cannot add a card, see "Plan B: Skip Storage" at the bottom.
3. 📋 **COPY YOUR BUCKET NAME** from the top, e.g. `verde-tech-v3.firebasestorage.app`
   (older projects show `verde-tech-v3.appspot.com` — either is fine, just copy
   exactly what YOUR console shows).

## Step 1.6 — Paste the Storage Rules
1. In Storage → **"Rules"** tab → replace everything with (from `firebase/storage.rules`):

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```
2. **Publish**. ✅ Leaf scans are publicly viewable (so the dashboard can render
   them) but only your backend can write.

## Step 1.7 — Enable Anonymous Authentication
1. Sidebar → **Build → Authentication** → **Get started**.
2. **"Sign-in method"** tab → click **"Anonymous"** → toggle **Enable** → **Save**. ✅
   (This is what lets judges use the app instantly with zero login.)

## Step 1.8 — Register the Web App & get client keys
1. Click the **⚙️ gear → Project settings** (top of sidebar).
2. Scroll to **"Your apps"** → click the **`</>`** (Web) icon.
3. App nickname: `verde-dashboard` → do NOT tick Firebase Hosting → **Register app**.
4. 📋 **COPY the entire `firebaseConfig` object** shown. It looks like:

```js
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "verde-tech-v3.firebaseapp.com",
  databaseURL: "https://verde-tech-v3-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "verde-tech-v3",
  storageBucket: "verde-tech-v3.firebasestorage.app",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abc123..."
};
```
Keep this open — these values map 1:1 into your `.env.local` in Part 3.
> If `databaseURL` is missing from the snippet, use the URL you copied in Step 1.2.

## Step 1.9 — Get the Admin Service Account key (for the backend)
1. Still in **Project settings** → **"Service accounts"** tab.
2. Click **"Generate new private key"** → **Generate key**.
3. A JSON file downloads (e.g. `verde-tech-v3-firebase-adminsdk-xxxxx.json`).
   🔒 **GUARD THIS FILE. Never commit it, never share it, never upload it.**
4. Open it in a text editor. You need 3 values from it:
   - `project_id`
   - `client_email`
   - `private_key`  (the long block starting `-----BEGIN PRIVATE KEY-----\n...`)

## Step 1.10 — Get the Legacy Database Secret (for the ESP32 boards)
The ESP32 firmware uses the Mobizt library's legacy-token auth:
1. **Project settings → Service accounts → "Database secrets"** tab.
2. Click **"Show"** next to your database → 📋 copy the secret string.
   > If you see "no secrets", click **Add secret**.
3. This is your firmware's `FIREBASE_AUTH` value.

> ⚠️ **Security note:** legacy secrets bypass your rules (full admin). That's
> exactly why our RTDB rules can stay strict for everyone else — the two
> ESP32 boards authenticate with this master secret. Never put it anywhere
> except inside the two `.ino` files that get flashed onto the chips.

---

# PART 2 — THIRD-PARTY API KEYS (3 free signups)

## 2.1 OpenWeatherMap (weather override)
1. https://home.openweathermap.org/users/sign_up → create account.
2. After login: profile menu → **"My API keys"** → copy the default key
   (or Create key: `verde`).
3. ⏳ New keys take **10 min – 2 hours** to activate. Test later with:
   `https://api.openweathermap.org/data/2.5/weather?lat=28.6139&lon=77.209&appid=YOUR_KEY`
4. Free tier: 1,000 calls/day. Our hourly cron uses 24/day. ✅

## 2.2 Plant.id (leaf disease AI)
1. https://web.plant.id → **"Get API key"** / sign up.
2. The free trial gives ~100 identification credits — plenty for the exhibition.
3. Copy the API key from your dashboard/confirmation email.

## 2.3 Google Gemini (conversational remedy AI)
1. https://aistudio.google.com → sign in with Google.
2. Click **"Get API key"** → **"Create API key"** → copy it.
3. Free tier covers Gemini 2.0 Flash generously. ✅

## 2.4 Make up two secrets yourself
Generate two random strings (run this twice in any terminal):
```bash
openssl rand -hex 24
```
- First one = `CAM_UPLOAD_API_KEY` (shared between the Vercel API & the ESP32-CAM)
- Second one = `CRON_SECRET` (protects the cron routes)

---

# PART 3 — LOCAL APP CONFIG & FIRST RUN

## 3.1 Create `.env.local`
In the `verde-app/` folder:
```bash
cp .env.example .env.local
```
Fill it using everything you copied above. Exact mapping:

| .env.local variable | Where you got it |
| :--- | :--- |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Step 1.8 → `apiKey` |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Step 1.8 → `authDomain` |
| `NEXT_PUBLIC_FIREBASE_DATABASE_URL` | Step 1.2 / 1.8 → `databaseURL` |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Step 1.8 → `projectId` |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Step 1.8 → `storageBucket` |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Step 1.8 → `messagingSenderId` |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | Step 1.8 → `appId` |
| `FIREBASE_PROJECT_ID` | Step 1.9 JSON → `project_id` |
| `FIREBASE_CLIENT_EMAIL` | Step 1.9 JSON → `client_email` |
| `FIREBASE_PRIVATE_KEY` | Step 1.9 JSON → `private_key` ⚠️ see below |
| `FIREBASE_STORAGE_BUCKET` | Step 1.5 bucket name |
| `FIREBASE_DATABASE_URL` | same as the NEXT_PUBLIC one |
| `CAM_UPLOAD_API_KEY` | Step 2.4 secret #1 |
| `PLANT_ID_API_KEY` | Step 2.2 |
| `GEMINI_API_KEY` | Step 2.3 |
| `OPENWEATHER_API_KEY` | Step 2.1 |
| `CRON_SECRET` | Step 2.4 secret #2 |

⚠️ **The `FIREBASE_PRIVATE_KEY` gotcha:** copy the whole value from the JSON
**including the quotes**, keeping the `\n` sequences exactly as they are:
```
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n"
```
Our `lib/firebaseAdmin.js` converts the `\n` back to real newlines automatically.

## 3.2 Run it
```bash
npm install
npm run dev
```
Open **http://localhost:3000/dashboard**:
- Purple "DEMO MODE" badge → env vars not loading (check filename is exactly
  `.env.local`, restart `npm run dev`).
- "AWAITING TELEMETRY…" badge → ✅ **PERFECT!** You are live-connected to
  Firebase; it's just waiting for the ESP32's first write.
- Quick proof: in the Firebase console → Data tab → manually change
  `sensors/moisture` to `70` → watch the gauge move **instantly**. 🎉

---

# PART 4 — DEPLOY TO VERCEL (production)

## 4.1 Push to GitHub
```bash
cd verde-app
git init && git add . && git commit -m "Verde Tech V3.0 web client"
```
Create an **empty private repo** on GitHub (e.g. `verde-tech-app`), then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/verde-tech-app.git
git branch -M main
git push -u origin main
```
(`.gitignore` already excludes `.env.local` — verify with `git status` that no
env file was staged!)

## 4.2 Import into Vercel
1. https://vercel.com → sign up **with GitHub** → **Add New → Project**.
2. Import `verde-tech-app`. Framework auto-detects as Next.js. Don't build yet —
   first click **"Environment Variables"** on the import screen.

## 4.3 Add ALL env vars to Vercel
Add **every single variable** from your `.env.local` (all 17). Two ways:
- **Fast way:** Vercel's env var screen accepts pasting your whole `.env.local`
  file into the first field — it auto-splits all of them.
- Manual: add one by one, exactly the same names & values.
Then click **Deploy**. ⏱️ ~2 minutes.

## 4.4 Note your production URL
e.g. `https://verde-tech-app.vercel.app` — the CAM firmware needs it.
`vercel.json` has already registered your two crons automatically
(hourly weather-sync, nightly cleanup-storage) — see the **Settings → Crons**
tab of your Vercel project to confirm.

## 4.5 Authorize the domain in Firebase
1. Firebase console → **Authentication → Settings → Authorized domains**.
2. **Add domain** → `verde-tech-app.vercel.app` (your actual domain). ✅
   (Without this, Anonymous Auth is rejected in production — the red banner.)

## 4.6 Test production
- Open `https://YOUR-APP.vercel.app/dashboard` → should show "AWAITING TELEMETRY…"
- Test the weather cron by hand:
  ```bash
  curl -H "Authorization: Bearer YOUR_CRON_SECRET" https://YOUR-APP.vercel.app/api/weather-sync
  ```
  → should return `{"success":true,"weather":"...","override_written":0}` and
  the dashboard weather badge updates to live Delhi weather. 🎉
- Test the upload guard:
  ```bash
  curl -X POST https://YOUR-APP.vercel.app/api/upload-photo -H "x-api-key: wrong" --data-binary "x"
  ```
  → must return `{"success":false,"error":"Invalid API Key header"}` ✅

---

# PART 5 — FLASH THE TWO ESP32 BOARDS

## 5.1 Code_1_Main_Brain.ino (ESP32 DevKit V1)
Edit the 4 config lines at the top:
```cpp
#define WIFI_SSID     "AaravsHotspot"          // your phone hotspot name
#define WIFI_PASSWORD "hotspot-password"
#define FIREBASE_HOST "verde-tech-v3-default-rtdb.asia-southeast1.firebasedatabase.app"
#define FIREBASE_AUTH "THE_DATABASE_SECRET_FROM_STEP_1.10"
```
> ⚠️ `FIREBASE_HOST` = your DB URL **without** `https://` and without any
> trailing `/`. Just the hostname.

Arduino IDE: Board **"DOIT ESP32 DEVKIT V1"**, port COM7, upload speed 921600.
Libraries needed (Library Manager): **DHT sensor library** (Adafruit) and
**Firebase ESP32 Client by Mobizt**. → **Upload**.

Open Serial Monitor @115200 → you should see:
```
WiFi Connected successfully!
Firebase Realtime Database handshake complete.
TELEMETRY -> Moisture: 52% | Temp: 24.5C | Tank: 85% | Light: 800 LUX
```
…and your **dashboard gauges come alive within 4 seconds**. 🎉

## 5.2 Code_2_ESP32_CAM.ino (AI-Thinker ESP32-CAM)
Edit the 6 config lines:
```cpp
#define WIFI_SSID      "AaravsHotspot"
#define WIFI_PASSWORD  "hotspot-password"
#define FIREBASE_HOST  "verde-tech-v3-default-rtdb.asia-southeast1.firebasedatabase.app"
#define FIREBASE_AUTH  "THE_DATABASE_SECRET_FROM_STEP_1.10"
#define UPLOAD_URL     "https://YOUR-APP.vercel.app/api/upload-photo"   // NEVER localhost!
#define UPLOAD_API_KEY "SECRET_#1_FROM_STEP_2.4"   // must equal CAM_UPLOAD_API_KEY on Vercel
```
Board: **"AI Thinker ESP32-CAM"**, upload speed 115200. → Upload → press RST.

**End-to-end test:** dashboard → **SCAN PLANT FOLIAGE** → within ~5s the CAM
flashes, posts the JPEG, the spinner releases, the photo appears in the
viewport, and Verde AI prints the Gemini diagnosis in the terminal. 🏆

---

# PART 6 — (OPTIONAL) DEPLOY RULES FROM CODE via Firebase CLI

Instead of console copy-paste, you can push both rule files from the repo
(they're wired up in `firebase.json`):

```bash
npm install -g firebase-tools
firebase login                      # opens browser
cd verde-app
firebase use --add                  # pick verde-tech-v3, alias: default
firebase deploy --only database     # pushes firebase/database.rules.json
firebase deploy --only storage      # pushes firebase/storage.rules
```
Now your security rules are version-controlled — change the file, redeploy. ✅

---

# 🚨 TROUBLESHOOTING TABLE

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Purple DEMO badge in production | Env vars missing on Vercel | Add all `NEXT_PUBLIC_*` vars, **Redeploy** |
| Red "Security token rejected" | Domain not authorized | Part 4.5 — add Vercel domain to Firebase Auth |
| Gauges frozen at 0, badge "AWAITING…" | ESP32 not writing | Check Serial Monitor: Wi-Fi? FIREBASE_HOST typo? Secret wrong? |
| ESP32 Serial: `token is not ready` | Wrong `FIREBASE_AUTH` or `FIREBASE_HOST` has `https://` in it | Use bare hostname + legacy DB secret |
| Scan spinner times out after 45s | CAM offline / wrong UPLOAD_URL / wrong API key | CAM Serial Monitor shows the POST result; verify URL & `x-api-key` match |
| Upload returns 401 | `UPLOAD_API_KEY` ≠ `CAM_UPLOAD_API_KEY` | Make them identical, redeploy + reflash |
| analyze-plant 500 | Plant.id/Gemini key invalid or quota out | Test keys with curl; check Vercel function logs |
| Weather badge stuck "—" | OWM key not activated yet | Wait up to 2h, or hit /api/weather-sync manually |
| `EDGE OFFLINE` while board runs | `last_updated` not updating: RTDB region URL wrong on board | Ensure firmware host = exact regional URL |
| Storage upload error `bucket does not exist` | Bucket name mismatch | `FIREBASE_STORAGE_BUCKET` must match Step 1.5 exactly |

---

# 🅱️ PLAN B: Skip Storage (if you can't enable Blaze/card)

**Already built in — zero code changes needed!** The upload route uses a
two-tier strategy automatically:

1. **Tier 1:** tries Firebase Storage (`/scans/` bucket upload).
2. **Tier 2 (automatic fallback):** if Storage fails for ANY reason (no Blaze
   plan, bucket missing, permission error), the JPEG is stored as a **base64
   data-URL directly inside RTDB** at `latest_scan.imageDataUrl`. The dashboard
   viewport and the AI analysis chain both handle this transparently.

To **force** Plan B and skip Storage entirely (e.g. you never enabled it),
just add one env var on Vercel:
```
PHOTO_STORAGE_MODE=rtdb
```
Notes:
- SVGA scans (~60KB) become ~80KB of base64 — trivial for RTDB.
- The fallback caps images at 400KB raw; if the CAM ever exceeds that, lower
  `jpeg_quality` (higher number) or `frame_size` in `Code_2_ESP32_CAM.ino`.
- In Plan B mode you can skip **Steps 1.5 and 1.6** (Storage setup) completely,
  and the nightly cleanup cron simply has nothing to delete.
- Each new scan overwrites `latest_scan`, so RTDB never accumulates photos.

---

# ✅ FINAL LAUNCH CHECKLIST

- [ ] RTDB created (Singapore) + rules published + seed imported
- [ ] Storage enabled + rules published
- [ ] Anonymous Auth ON
- [ ] Web app registered, client keys copied
- [ ] Service account JSON downloaded (and kept secret!)
- [ ] Database secret copied for firmware
- [ ] OWM + Plant.id + Gemini keys obtained
- [ ] `.env.local` filled → local dashboard says "AWAITING TELEMETRY…"
- [ ] Repo pushed → Vercel deployed with all 17 env vars
- [ ] Vercel domain added to Firebase Auth authorized domains
- [ ] weather-sync curl test passes
- [ ] Main Brain flashed → gauges live
- [ ] ESP32-CAM flashed → Scan button → photo + AI diagnosis end-to-end
- [ ] Crons visible in Vercel Settings → Crons

**When every box is ticked, Project Verde V3.0 is fully operational. 🏆**
