# 10. Database Rules & RLS Security

This document details the security rules deployed on your Firebase Realtime Database and Cloud Storage buckets to secure your data.

---

## 🔒 1. Firebase Realtime Database Security Rules

These rules ensure that only authenticated sessions (such as your Next.js app running under Anonymous Auth, or your ESP32 board using a secure Master Secret Key) can read and write to your nodes.

```javascript
{
  "rules": {
    "Garden": {
      // Only authenticated users can read sensor values
      ".read": "auth != null",
      // Only authenticated users/ESP32 can write telemetry
      ".write": "auth != null"
    }
  }
}
```

---

## 🔒 2. Firebase Cloud Storage Security Rules

To ensure leaf scans are securely handled while allowing public rendering on your Next.js dashboard viewport, set these rules on your Storage buckets:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /scans/{allPaths=**} {
      // Leaf scans are publicly readable so your dashboard can load images via URLs
      allow read: if true;
      
      // Only authenticated users or your backend API can write photos
      allow write: if request.auth != null;
    }
  }
}
```

---

## 🕵️‍♂️ 3. Best Practices
* **No Public Writing:** Never leave rules set to `".write": "true"` in production. This leaves your water pump and grow lights completely open to anyone on the internet who scans your website!
* **Secret Rotation:** Store your Firebase Admin secret keys securely inside Vercel environment variables, and never commit them to public GitHub repositories.
