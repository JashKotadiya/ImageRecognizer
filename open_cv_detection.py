import cv2

thres = 0.45 #Threshold to detect object

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(10, 70)

classNames = []
classFile = "YOUR-FILE.names"
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip("\n").split('\n')

configPath = 'ssd_mobilnet_v3_large_coco_2020_01_14.pbtxt'
