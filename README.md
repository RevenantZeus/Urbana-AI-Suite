# 🛍️ Urbana AI Suite - Virtual Assistant & Body Scanner

An end-to-end, real-time AI fashion assistant and computer vision body measurement platform built for **Urbana Closet**. 

The system provides an instant AI personal stylist interface paired with real-time browser-based skeletal landmark tracking to recommend custom apparel cuts and match users with local partner tailors.

---

## 🌟 Key Features

- **⚡ Real-Time AI Stylist Chat:** Asynchronous Python WebSocket server (`backend/app.py`) providing low-latency fashion recommendations via the Google GenAI SDK.
- **🛡️ Multi-Model Fallback Pipeline:** Automatic server-side failover routing across `gemini-3.8-flash`, `gemini-3.6-flash`, and `gemini-3.5-flash-lite` to ensure high availability during API load spikes.
- **📐 Client-Side Body Scanner:** In-browser pose estimation powered by MediaPipe Pose CDN tracking 33 key 3D landmarks (shoulders, hips) at zero server compute cost.
- **🧵 Smart Tailor Matcher:** Automated proportion-based routing that maps live body ratios (shoulder-to-hip ratio) to partner tailor specialties stored in `tailors.json`.
- **🎨 Rendered UI & Stream Control:** Clean frontend interface featuring `marked.js` Markdown parsing, responsive layout, and full webcam lifecycle (start/stop) controls.

---

## 🏗️ Project Architecture

* **backend/**
  * `app.py` — Async WebSocket Server & Gemini API Router
  * `tailors.json` — Partner Tailor Catalog Data
  * `.env.example` — Environment template (No secrets)
  * `requirements.txt` — Python dependencies
* **frontend/**
  * `index.html` — Web client UI & MediaPipe Pose tracker
* `.gitignore` — Ignores .env and build artifacts
* `README.md` — Documentation

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation & Setup

1. **Clone the Repository:**
   `git clone [https://github.com/RevenantZeus/Urbana-AI-Suite.git](https://github.com/RevenantZeus/Urbana-AI-Suite.git)`
   `cd Urbana-AI-Suite`

2. **Install Backend Dependencies:**
   `cd backend`
   `pip install -r requirements.txt`

3. **Configure Environment Variables:**
   Copy `.env.example` to `.env` in the `backend/` folder: `cp .env.example .env`
   *Edit `.env` and set `GEMINI_API_KEY=your_actual_key`.*

4. **Run the Backend Server:**
   `python app.py`

5. **Launch the Frontend:**
   Open `frontend/index.html` directly in any web browser.