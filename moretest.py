import os
import time
import cv2
import sys
import pygame
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------------------
# Setup & Initialization
# ----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ Missing GOOGLE_API_KEY in .env file")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Optional: initialize pygame for audio feedback
pygame.mixer.init()
CAMERA_INDEX = 0
SAVE_IMAGES = True  # Change to False if you don’t want to store frames

# ----------------------------
# Helper Functions
# ----------------------------
def capture_and_analyze(frame):
    """Capture an image and send to Gemini for analysis."""
    try:
        # Convert to RGB for PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Optional: save the image
        if SAVE_IMAGES:
            os.makedirs("captures", exist_ok=True)
            filename = f"captures/capture_{int(time.time())}.jpg"
            img.save(filename)

        print("📸 Captured frame, analyzing with Gemini...")
        response = model.generate_content([
            "Describe what you see in the image in under 12 words. "
            "Be vivid, specific, and mention colors or objects clearly.",
            img
        ])
        description = response.text.strip() if response.text else "(No response)"
        print("\n🤖 Gemini says:", description, "\n")
        return description
    except Exception as e:
        print("⚠️ Error analyzing frame:", e)
        return None

def overlay_text(frame, text, pos=(20, 40), color=(255, 255, 255), scale=0.8, thickness=2):
    """Overlay readable text on video frame."""
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 2)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

# ----------------------------
# Main Function
# ----------------------------
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        sys.exit(1)

    print("🎥 Press SPACE to capture an image, or Q to quit.")
    last_description = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        # Display live feed with overlay instructions
        overlay_text(frame, "Press SPACE to capture, Q to quit", (20, 30))
        if last_description:
            overlay_text(frame, f"Gemini: {last_description[:60]}...", (20, 60), color=(0, 255, 0), scale=0.6)

        cv2.imshow("Gemini Vision", frame)
        key = cv2.waitKey(1) & 0xFF

        # Capture frame
        if key == 32:  # SPACE
            overlay_text(frame, "⏳ Analyzing...", (20, 90), color=(0, 200, 255))
            cv2.imshow("Gemini Vision", frame)
            cv2.waitKey(100)
            last_description = capture_and_analyze(frame)
            time.sleep(1)
        elif key == ord('q'):
            print("👋 Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    main()
