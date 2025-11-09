import cv2
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time
import pygame

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apiKey)

# Load the model
model = genai.GenerativeModel("gemini-2.5-flash")
gemini_confidence = 0
user_description = input("Describe the object you lost: ")

classNames = []
classFile = "C:/Users/Jash_/OneDrive/Desktop/HackUmass/ImageRecognizer/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "C:/Users/Jash_/OneDrive/Desktop/HackUmass/ImageRecognizer/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "C:/Users/Jash_/OneDrive/Desktop/HackUmass/ImageRecognizer/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    if len(objects) == 0: objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className == "person": 
                continue
            if className in objects:
                objectInfo.append([box, className])
                # if draw:
                #     cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                #     cv2.putText(img, className.upper(), (box[0]+10, box[1]+30),
                #         cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                #     cv2.putText(img, str(round(confidence*100,2)), (box[0]+200, box[1]+30),
                #         cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

    return img, objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    prev_detected = set()

    while True:
        success, img = cap.read()
        if not success:
            break

        result_img, objectInfo = getObjects(img, 0.70, 0.2)

        detected_this_frame = set()

        for box, obj_name in objectInfo:
            if obj_name not in detected_this_frame:
                # Prepare the current img for Gemini
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                time.sleep(2.5)
                # Send image and prompt to Gemini
                response = model.generate_content([
                    f"Describe the object in this image in less than 10 words, be detailed but concise, ignore any people in the frame.",
                    pil_img
                ])

                print(f"\nGemini description for:")
                gemini_response = response.text #Saves the response
                print(gemini_response)
                
                print("Working patt 1")
                gemini_confidence = model.generate_content([
                    f"Imagine you are hired to compare two descriptions of objects and determine how close the descriptions match. Here is the first description: {user_description}. Here is the second description {gemini_response}. Return only the confidence level as an integer between one and one hundred"])
                
                gemini_confidence = int(gemini_confidence.text)
                print("Was good")
                if gemini_confidence > 75:
                    print(f"Lost object Found with confidence {gemini_confidence}!!")
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.mixer.init()

                    # Load your short sound file (make sure you have it in your folder)
                    pygame.mixer.music.load("beep.wav")
                    pygame.mixer.music.play()

                    # Wait a short amount of time (in seconds), adjust as needed
                    time.sleep(2)

                    # Stop music if still playing
                    pygame.mixer.music.stop()
                    break
                else: 
                    print(f"Not enough confidence: {gemini_confidence}")

                detected_this_frame.add(obj_name)  

        prev_detected = detected_this_frame.copy()

        cv2.imshow("Output", result_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break