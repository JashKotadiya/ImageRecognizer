import google.generativeai as genai
from PIL import Image
import time
import cv2
import pygame
import sys

genai.configure(api_key="AIzaSyCJmPxUv36qoucvBFQ7-TWDW8kGjRkc_Go")
model = genai.GenerativeModel("gemini-2.5-flash")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

print("Press SPACE to capture an image, or ESC to quit.")

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
            "Describe what you see in this image.",
            img
        ])

        print("\nGemini says:")
        print(response.text)
        print("\nPress SPACE to capture again, or ESC to quit.\n")

        time.sleep(1)  # avoid spam-clicking
    # ESC key -> exit
    elif key == pygame.K_x:  # ESC
        sys.quit()

# Use gemini 
# Otherwise use the Max thing, but you have to train your own model -> When the cloud is not access
# Focus on the storing telling 
# Jewel collection because camera is pointing at the floor
# Tell a story about the problem you are trying to solve 
