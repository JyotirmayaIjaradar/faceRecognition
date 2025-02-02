''''
Real time face recognition using different method for raspberry pi and some application like security.
Developed by Jyotirmaya Ijaradar and Jinjing Xu.

'''

import cv2
import numpy as np
import csv
import os
import RPi.GPIO as GPIO 
from time import sleep

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW) # Set pin 5 to be an output pin and set initial value to low (off)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Downloads/faceRecognition/trainer/trainer.yml')
cascadePath = "/home/pi/Downloads/faceRecognition/faceRecognition/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = []
with open('/home/pi/Downloads/faceRecognition/b.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            names.append(row[0])

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            GPIO.output(5, GPIO.HIGH) # Turn on
            sleep(1) # Sleep for 1 second
            GPIO.output(5, GPIO.LOW) # Turn off
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
