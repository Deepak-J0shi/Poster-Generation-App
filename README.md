# **Salon Poster Generator App**

A full-stack mobile application that allows salons and small businesses to instantly generate professional marketing posters using a clean mobile UI and a backend-driven image generation system.
<img width="540" height="587" alt="image" src="https://github.com/user-attachments/assets/2c3b7f18-0ef3-48b7-af6f-7b790f489579" />

---

## **Features**

* Mobile-first user interface built with Expo (React Native)
* Simple form to enter salon or brand details
* Instant poster generation as high-quality PNG images
* Live preview of generated posters inside the app
* Ability to share or save posters directly from the device
* Fast and lightweight client with all heavy processing handled on the server

---

## **UI Overview**

The app follows a clean, minimal, and business-focused design aimed at:

* Easy user input
* Clear call-to-action
* Immediate visual feedback

App screenshots (home screen, form input, and generated poster) will be displayed here.

---

## **Tech Stack**

### **Frontend (Mobile App)**

* Expo (React Native)
* JavaScript
* Expo FileSystem and Sharing APIs
* Linear Gradient UI components

### **Backend (Server)**

* FastAPI (Python)
* Pillow (PIL) for image generation
* Uvicorn ASGI server
* CORS-enabled REST API

---

## **Project Structure**

```
.
├── Backend/        # FastAPI backend (poster generation logic)
├── Frontend-App/   # Expo mobile application
└── README.md
```

Each folder contains its own detailed README with setup and usage instructions.

---

## **Use Cases**

* Salon and beauty businesses
* Small local brands
* Marketing creatives
* Quick promotional poster generation

---

## **Notes**

* Frontend and backend are intentionally decoupled
* Poster image rendering is handled entirely on the server for consistent output
* The architecture is designed to be extensible for future features such as themes, templates, and branding options

---
