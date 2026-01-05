# **Salon Poster Generator (Expo Mobile App)**

A React Native mobile application built using **Expo** that allows users to generate professional salon posters by submitting brand details to a FastAPI backend. The app sends form data, receives a generated poster image, previews it instantly, and allows users to save or share the result.

---

# **Table of Contents**

1. [Overview](#overview)
2. [Features](#features)
3. [Folder Structure](#folder-structure)
4. [How to Run Locally](#how-to-run-locally)

   * Prerequisites
   * Installation
   * Running the app
   * Backend connectivity
5. [API Integration](#api-integration)
6. [Architecture & Data Flow](#architecture--data-flow)
7. [Key Design Decisions](#key-design-decisions)

---

# **Overview**

This project is a **mobile poster generation app** designed for salons and small businesses.

The app:

* Collects brand details (salon name, offer text)
* Sends data to a FastAPI backend via multipart form request
* Receives a generated **PNG poster image**
* Displays the poster inside the app
* Allows users to **save or share** the poster

The frontend is intentionally kept lightweight and backend-driven, with **all image generation handled server-side**.

---

# **Features**

✔ Built using **Expo (React Native)**
✔ Clean mobile-first UI
✔ Multipart form submission to backend
✔ Handles binary image responses
✔ Local preview of generated poster
✔ Share / save functionality using native OS APIs
✔ Works without Android Studio or Xcode

---

# **Folder Structure**

```
frontend/
│
├── assets/                 # App assets (icons, images)
├── App.js                  # Main application logic
├── app.json                # Expo configuration
├── index.js                # App entry point
├── package.json            # Dependencies & scripts
├── package-lock.json
└── README.md
```

---

# **How to Run Locally**

---

## **1. Prerequisites**

Make sure you have:

* Node.js (LTS recommended)
* npm
* Expo Go app installed on your mobile device

Check versions:

```bash
node -v
npm -v
```

---

## **2. Installation**

```bash
cd frontend
npm install
```

---

## **3. Running the App**

```bash
npx expo start --tunnel
```

This will:

* Start the Expo Metro bundler
* Generate a QR code
* Allow the app to run on a physical device via **Expo Go**

> **Recommended:** Use `--tunnel` to avoid local network and HTTP restrictions.

---

## **4. Backend Connectivity**

Update the backend API URL inside `App.js`:

```js
const API_URL = "http://<YOUR_LOCAL_IP>:8000/generate";
```

Example:

```js
const API_URL = "http://10.143.26.188:8000/generate";
```

Ensure:

* Backend is running
* `/health` endpoint is accessible
* Mobile and backend can communicate (or use tunnel mode)

---

# **API Integration**

### Endpoint Used

```
POST /generate
```

### Request Type

```
multipart/form-data
```

### Fields Sent

* `salonName` (required)
* `offer` (optional)

### Response

* Binary PNG image (`image/png`)

### Handling Strategy

* Response read as `arrayBuffer`
* Converted to base64
* Written to local cache
* Rendered using `<Image />`

---

# **Architecture & Data Flow**

```text
User Input (Mobile App)
        ↓
Expo App (FormData)
        ↓
FastAPI Backend (/generate)
        ↓
Poster Image Generation
        ↓
PNG Bytes Response
        ↓
Expo App Preview + Share
```

---

# **Key Design Decisions**

### 1. Server-side Image Generation

All poster rendering is handled by the backend to:

* Keep the mobile app lightweight
* Avoid font/image rendering issues on devices

### 2. Binary Image Transfer

The app directly consumes PNG bytes instead of base64 JSON to:

* Reduce payload size
* Preserve image quality

### 3. Expo over React Native CLI

Chosen for:

* Faster setup
* No native build requirement
* Easy device testing via Expo Go

---
