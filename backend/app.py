import os
import json
import asyncio
import websockets
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY is missing from backend/.env!")
    ai_client = None
else:
    print("✅ GEMINI_API_KEY detected! Initializing client...")
    ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Load Local Partner Tailors Catalog
TAILORS_FILE = os.path.join(os.path.dirname(__file__), 'tailors.json')
try:
    with open(TAILORS_FILE, 'r', encoding='utf-8') as f:
        TAILORS_CATALOG = json.load(f)
    print(f"🧵 Loaded {len(TAILORS_CATALOG)} local partner tailors from tailors.json")
except Exception as e:
    print(f"⚠️ Could not load tailors.json: {e}")
    TAILORS_CATALOG = []

# Supported active text model endpoints
TARGET_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]

async def generate_with_fallback(prompt, system_instruction):
    """Loops through active models if 503 high demand or 429 rate limit occurs."""
    last_error = None
    
    for model_name in TARGET_MODELS:
        try:
            print(f"🔄 Requesting model: {model_name}...")
            response = await ai_client.aio.models.generate_content(
                model=model_name,
                contents=f"{system_instruction}\nUser: {prompt}"
            )
            print(f"🟢 Success using model: {model_name}!")
            return response.text
        except Exception as e:
            err_msg = str(e)
            print(f"⚠️ Model {model_name} failed: {err_msg}")
            last_error = e
            if "503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg:
                continue
            else:
                raise e

    raise last_error if last_error else RuntimeError("All candidate models are busy.")

async def handle_ai_stylist(websocket, prompt):
    if not ai_client:
        await websocket.send(json.dumps({
            "type": "ai_stylist_response",
            "status": "error",
            "message": "Gemini API client is not initialized. Check backend/.env."
        }))
        return

    try:
        print(f"📩 Processing stylist prompt: {prompt}")
        system_instruction = (
            "You are Urbana AI, a personal fashion assistant for Urbana Closet. "
            "Help customers find clothes, tailors, or styles concisely and helpfully."
        )
        reply_text = await generate_with_fallback(prompt, system_instruction)
        
        await websocket.send(json.dumps({
            "type": "ai_stylist_response",
            "status": "success",
            "text": reply_text
        }))
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        await websocket.send(json.dumps({
            "type": "ai_stylist_response",
            "status": "error",
            "message": str(e)
        }))

async def handle_tailor_matcher(websocket, measurements):
    """Processes MediaPipe landmarks and matches with local partner tailors from catalog."""
    if not ai_client:
        return

    try:
        print(f"📩 Processing tailor match for: {measurements}")
        
        tailor_catalog_str = json.dumps(TAILORS_CATALOG, indent=2)
        
        system_instruction = (
            f"You are Urbana AI's Custom Tailoring Assistant for Urbana Closet.\n"
            f"Here is our active partner tailor catalog:\n{tailor_catalog_str}\n\n"
            "INSTRUCTIONS:\n"
            "1. Analyze the user's body landmark ratios (shoulder span, hip span, shoulder-to-hip ratio).\n"
            "2. Recommend 1-2 optimal fit/silhouette styles (e.g., Athletic Broad-Shoulder V-Cut, Slim Fit, Tailored Kurta).\n"
            "3. Recommend 1-2 SPECIFIC partner tailors from the catalog that best match their body structure and ratio, "
            "including tailor name, location, turnaround time, and why they fit this specific ratio.\n"
            "Keep the response concise, polished, and structured with bullet points."
        )
        
        reply_text = await generate_with_fallback(measurements, system_instruction)
        
        await websocket.send(json.dumps({
            "type": "ai_stylist_response",
            "status": "success",
            "text": reply_text
        }))
    except Exception as e:
        print(f"❌ Error during tailor matching: {e}")

async def router(websocket):
    print("⚡ Client connected to Urbana WSServer!")
    try:
        async for message in websocket:
            print(f"📥 Received frame: {message}")
            payload = json.loads(message)
            event_type = payload.get("type")

            if event_type == "ai_stylist_query":
                await handle_ai_stylist(websocket, payload.get("prompt", ""))
            elif event_type == "tailor_match_query":
                await handle_tailor_matcher(websocket, payload.get("measurements", ""))
            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Unknown event type: {event_type}"
                }))
    except websockets.exceptions.ConnectionClosedError:
        print("🔌 Client disconnected.")

async def main():
    port = int(os.getenv("PORT", 8000))
    async with websockets.serve(router, "0.0.0.0", port):
        print(f"🚀 Urbana AI Server running on ws://localhost:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())