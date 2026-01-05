# **Salon Poster Generator (FastAPI Backend)**

A FastAPI-based backend service that dynamically generates high-quality salon posters as PNG images. It accepts brand details and optional logos via multipart form-data, renders posters using PIL, and returns the final image directly as a binary response.

---

# **Table of Contents**

1. [Overview](#overview)
2. [Features](#features)
3. [Folder Structure](#folder-structure)
4. [How to Run Locally](#how-to-run-locally)

   * Prerequisites
   * Installation
   * Running the server
5. [API Endpoints](#api-endpoints)
6. [Poster Generation Pipeline](#poster-generation-pipeline)
7. [Architecture & Design Decisions](#architecture--design-decisions)
8. [Error Handling](#error-handling)

---

# **Overview**

This backend service powers the **Salon Poster Generator App**.

It:

* Accepts poster content details from a mobile client
* Optionally accepts a logo (file upload or URL)
* Generates a branded poster using custom fonts and layouts
* Returns the final poster as a **PNG image**

All visual rendering logic is handled server-side to ensure:

* Consistent output quality
* Device-independent rendering
* Minimal frontend complexity

---

# **Features**

✔ Built with **FastAPI**
✔ Multipart form-data handling
✔ Dynamic image generation using **Pillow (PIL)**
✔ Custom font support
✔ Optional logo upload or remote logo fetch
✔ Returns raw PNG image bytes
✔ CORS-enabled for mobile/web clients

---

# **Folder Structure**

```
backend/
│
├── assets/                 # Static assets (backgrounds, templates)
├── main.py                 # FastAPI app & routes
├── poster.py               # Core poster generation logic
├── Poppins-Regular.ttf     # Custom font used in posters
├── requirements.txt        # Python dependencies
└── README.md
```

---

# **How to Run Locally**

---

## **1. Prerequisites**

Ensure you have:

* Python 3.9+
* pip
* Virtual environment support (recommended)

Check Python version:

```bash
python3 --version
```

---

## **2. Installation**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## **3. Running the Server**

```bash
python main.py
```

Server starts at:

```
http://0.0.0.0:8000
```

Health check:

```
GET /health
```

Expected response:

```json
{"status":"ok"}
```

---

# **API Endpoints**

---

## **POST /generate**

### Description

Generates a salon poster based on submitted form data and returns a PNG image.

### Request Type

```
multipart/form-data
```

### Response

* **Content-Type:** `image/png`
* **Body:** Raw PNG bytes

---

# **Poster Generation Pipeline**

```text
Incoming Request
        ↓
Form Validation
        ↓
Logo Resolution (Upload or URL)
        ↓
Poster Layout Rendering (PIL)
        ↓
PNG Byte Stream
        ↓
StreamingResponse to Client
```

Core logic resides in:

```python
create_poster(...)
```

---

# **Architecture & Design Decisions**

### 1. Binary Image Response

The API returns raw PNG bytes instead of base64 JSON to:

* Reduce payload size
* Improve performance
* Simplify frontend rendering

---

### 2. PIL-Based Rendering

Using Pillow ensures:

* Font control
* Image compositing
* Platform-independent rendering

---

### 3. Stateless API

No poster data is stored server-side:

* Improves scalability
* Avoids storage management
* Makes the service horizontally scalable

---

### 4. CORS Enabled

Allows seamless communication with:

* Expo mobile app
* Future web frontend

---

# **Error Handling**

| Scenario                 | Response                    |
| ------------------------ | --------------------------- |
| Missing salonName        | `400 Bad Request`           |
| Invalid logo file        | `400 Bad Request`           |
| Logo URL fetch failure   | `400 Bad Request`           |
| Internal rendering error | `500 Internal Server Error` |

Errors are returned as JSON with clear messages.

---
