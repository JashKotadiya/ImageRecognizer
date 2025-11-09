import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time
import json
from receiveimage import request_capture 
from sendmovement import send_command


load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apiKey)

#turning sutff
turns = 7
confidence = 0
dist = 100

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

user_description = input("Describe the object you lost: ")

while((confidence < 85 or dist < 0.2) and turns != 0):
    request_capture("172.31.192.171", 5001)
    time.sleep(6)

    # Load the static image
    img_path = "received.jpg"
    pil_img = Image.open(img_path)

    response = model.generate_content([
        f"Imagine you are hired to find an object. You have been given a description of the object, and a random image. If the object is found in the image, return your response as two number ONLY!. Your response should look like this and distance is in meters, example: 45,1. NOthing else should be returned, jsut these.  If the object is not found, use confidence 0 and distance -1. Here is the description: {user_description}, and here is the image", pil_img 
    ])

    print(response.text)

    result = (response.text)
    confidence, distance = int(result.split(',')[0]), float(result.split(',')[1])

    if confidence >= 85:
        print(f"\nLost object Found with confidence {confidence}!!")
    else:
        print(f"\nLost object not confidently found. Confidence: {confidence}")
    
    if(distance == -1):
        send_command('3')
        turns -= 1
    elif(distance > -1 and distance < 0.2):
        continue
    elif(distance > -1):
        send_command('1')
        turns = 6
