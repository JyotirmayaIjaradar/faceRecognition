''''
Real time face recognition using different method for raspberry pi and some application like security.
Developed by Jyotirmaya Ijaradar and Jinjing Xu.

'''

import cv2
import os
import csv
import numpy as np
import pandas as pd
import shutil

# Initialize raspi camera and set video resolution
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

# Set face detection object
#face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier("/home/pi/Downloads/faceRecognition/faceRecognition/haarcascade_frontalface_default.xml");

face_id = []
face_name = []

# Method to read csv file and save data to list
def read_csv(fname,rchoice):
    with open('/home/pi/Downloads/faceRecognition/'+ str(fname) + '.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        if rchoice == 1:
            for row in csvReader:
                face_id.append(row[0])
        
        elif rchoice == 2:
            for row in csvReader:
                face_name.append(row[0])


# Write list data to local file
def write_csv(temp,fname):
    df = pd.DataFrame(temp)
    df.to_csv("/home/pi/Downloads/faceRecognition/"+ str(fname) +".csv", mode = 'a', header = False, index = False)
        

# Generate face id based on the list
def get_face_id():
    size = len(face_id)
    return size;


# Print all the face name and their id
def show_existing_face_id():
    size = len(face_name)
    for i in range(size): 
        print('Face id : ' + str(i)+ '   Face name: ' + str(face_name[i]) + '\n' )


# Method to truncate csv file
def clear_csv(fname):
    f = open('/home/pi/Downloads/faceRecognition/'+ str(fname) + '.csv',"w+")
    f.close()

# Read if any existing face name and id
read_csv('a',1)
read_csv('b',2)

# Method for capturing or importing images for dataset
print('\n Please chose the way you want to store image for dataset: \n\n    a) "1" for pycamera capture \n    b) "2" for import from local storge ')
choice = input('    c) "3" for downloading through API (Work in Progress..):  ')
a = int(choice)

# For each person, enter one numeric face id
#face_id = input('\n please enter the face id for the person:  ')

print("\n\n\n To generate an unique face id kindly select any option below: ")
id_choice_raw = input("\n\n    a) Enter '1' if you want to store new face. \n    b) Enter '2' for existing face. \n :  ")
id_choice = int(id_choice_raw)

if id_choice == 1:
    face_id_temp = get_face_id()
    face_name_temp = input("\n\nYour face id has been generated, kindly enter your name:  ")
    face_id.append(face_id_temp)
    face_name.append(face_name_temp)
    face_id_list = [face_id_temp]
    face_name_list = [face_name_temp]
    write_csv(face_id_list,'a')
    write_csv(face_name_list,'b')
    print("\n\nThank you, "+ str(face_name_temp) + ". Your name has stored, now wait for the camera to capure your face! ")
    
elif id_choice == 2:
    show_existing_face_id()
    face_id_temp = input("\n\nKindly enter your face id based on above list:  ")
    
else:
    print("\n\nInvalid choice! ")
    
    
if a == 1:
    print("\n\n\n Initializing face capture. Kindly Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0
    
    while(True):
        
        ret, img = cam.read()
        img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("/home/pi/Downloads/faceRecognition/dataset/User." + str(face_id_temp) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            
            cv2.imshow('image', img)
            
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 60: # Take 60 face sample and stop video
            break
        
    # Do a bit of cleanup
    print("\n\n\n Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

elif a == 2:
    
    print("\n\n\n [Guide] Store your image file to the LocalImage folder and rename with 'sample.jpg' (/home/pi/Downloads/OpenCV-Face-Recognition-master/LocalImage/")
    op = input('\n If you already stored the image then press "y" otherwise "n":  ')
    if op == 'y' or op == 'Y':
        image_path = "/home/pi/Downloads/faceRecognition/LocalImage/sample.jpg"
        
    elif op == 'n' or op == 'N':
        image_path = input('\n\n Then ente the image directory manually. \n eg- "/home/pi/image.jpg" \n path:  ')
        
    else:
        print("Error!")
        
    # Initialize individual sampling face count
    count = 0
    
    print("\n\n Face detection task assigned. Please wait. . .")
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        # Save the face image into the datasets folder
        for i in range(60):
            count += 1
            cv2.imwrite("/home/pi/Downloads/faceRecognition/dataset/User." + str(face_id_temp) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            
    print("\n\n Done! All the images saved in the dataset directory")
    
    # Reset path, clean LocalImage folder and finish message
    shutil.rmtree('/home/pi/Downloads/faceRecognition/LocalImage')
    os.mkdir('/home/pi/Downloads/faceRecognition/LocalImage')
    print("\n\n\n The local image directory has cleaned, Exiting Program and Successfully dataset created")
    
elif a == 3:
    print("\n Work in progress!")

else:
    print("\n Invalid choice!")
