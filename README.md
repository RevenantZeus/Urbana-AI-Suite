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

```text
Urbana AI Suite/
├── backend/
│   ├── app.py           # Async WebSocket Server & Gemini API Router
│   ├── tailors.json     # Partner Tailor Catalog Data
│   ├── .env.example     # Environment template (No secrets)
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Web client UI & MediaPipe Pose tracker
├── .gitignore           # Ignores .env and build artifacts
└── README.md            # 

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/urbana-ai-suite.git](https://github.com/YOUR_USERNAME/urbana-ai-suite.git)
   cd urbana-ai-suite

2. **Intall Backend Dependencies**
    ```bash
    cd backend
    pip install websockets python-dotenv google-genai

3. **Configure Environment Variables:**
Copy .env.example to .env in the backend/ folder and insert your Gemini API Key:
    ```bash
    cp .env.example .env
Edit .env and set GEMINI_API_KEY=your_actual_key.

4. **Run the Backend Server:**
    ```bash
    python app.py
    
5. **Launch the Frontend:**
    Open frontend/index.html directly in any web browser.
    
6. **Launch the Frontend:**
    Open frontend/index.html directly in any web browser.