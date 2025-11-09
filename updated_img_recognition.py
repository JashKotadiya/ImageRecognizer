#Have Infrared sensor, along with a camera. We use computer vision (open cv)
#   Use the infrared sensor to check whether we are within 2 feet of a distance
#   stop the motor
#   Capture a frame from the camera
#   Send said frame to Gemini
#   Gemini identifies image, and provides a description
#   Send description to Gemini, along with user description
#   If the match is more than 85%, then the speaker blares (or something else happens)
#   Else, the robot will turn in some way, and continue

import RPi.GPIO as GPIO
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time
import cv2


load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apiKey)

# Load the model
model = genai.GenerativeModel("gemini-2.5-flash")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

print("Press SPACE to capture an image, or q to quit.")

SENSOR_PIN = 23  # Use GPIO 23, change as needed

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while GPIO.input(SENSOR_PIN) == 0:
         # LOW: Object detected
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        # Display the live feed
        cv2.imshow("Gemini Camera Feed", frame) # Remove later
    
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
        
except KeyboardInterrupt:
    GPIO.cleanup()