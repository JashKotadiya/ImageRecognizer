import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time
import cv2

# User description 
# OpenCV to detect an object 
# Ask Gemnini to see how much this matched 70% or 80% accuracy

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=apiKey)

# Load the model
model = genai.GenerativeModel("gemini-2.5-flash")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

print("Press SPACE to capture an image, or q to quit.")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Display the live feed
    cv2.imshow("Gemini Camera Feed", frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF

    # SPACE key -> capture and analyze frame
    if key == 32:  # SPACE
        print("📸 Captured frame, sending to Gemini...")

        # Convert OpenCV image (BGR → RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Send to Gemini for interpretation
        response = model.generate_content([
            "Describe the object or living thing you see in this image in less than 10 words, be detailed but concise.",
            img
        ])

        print("\nGemini says:")
        print(response.text)
        print("\nPress SPACE to capture again, or Q to quit.\n")

        time.sleep(1)  # avoid spam-clicking
    # Q key -> exit
    elif key == ord("q"):  # Q
        break

cap.release()
cv2.destroyAllWindows()