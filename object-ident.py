import cv2
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apiKey)

# Load the model
model = genai.GenerativeModel("gemini-2.5-flash")

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
                print(response.text)

                detected_this_frame.add(obj_name)

        prev_detected = detected_this_frame.copy()

        cv2.imshow("Output", result_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
