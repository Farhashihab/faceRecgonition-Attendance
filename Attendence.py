import os
import datetime as dt
from datetime import datetime
import time

import cv2
import face_recognition
import numpy as np
import pyttsx3
# import pythoncom

# import speech_recognition as sr

with open('Attendence.csv', 'w')as file:
    today2 = dt.date.today()
    # dtString = now.strftime('%H:%M:%S')
    file.writelines(f'Date : {today2}')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#
# #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


path = "AttendenceImages"
images = []
imagesNames = []

myList = os.listdir(path)

print(myList)

for img in myList:
    curImg = cv2.imread(f'{path}/{img}')
    images.append(curImg)
    imagesNames.append(os.path.splitext(img)[0])

print(imagesNames)


# functin for encoding our given images

def doEncoding(images):
    encodeList = []
    for img in images:
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(RGBimg)[0]
        encodeList.append(encode)

    return encodeList


storeName = []


def storeNames(name):
    storeName.append(name)


print(storeName)


def takeAttendence(name):
    with open('Attendence.csv', 'r+')as file:
        myDataList = file.readlines()
        print(f'Data List{myDataList}')
        print(f'attendence{myDataList}')
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            y = 'Yes'
            N = 'NO'
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            # today =  datetime.today()
            # # if today not in nameList:
            # #     file.writelines(f"Date {today}")

            file.writelines(f'\n{name},{dtString},{y}')


# takeAttendence('Elon')


encodeListKnown = doEncoding(images)
print(len(encodeListKnown))
print('Encode Completed')

cap = cv2.VideoCapture(0)
names = []

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceMatche = []
    faceInCuFrame = face_recognition.face_locations(imgS)
    encodeCuFrame = face_recognition.face_encodings(imgS, faceInCuFrame)

    for encodeFaces, faceLoc in zip(encodeCuFrame, faceInCuFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFaces)
        # faceMatche.append(matches)
        # print(faceMatche)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFaces)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)
        print(matchIndex)

        if matches[matchIndex]:
            name = imagesNames[matchIndex].upper()
            # print(name)
            names.append(name)
            # print(names)

            # for i in names:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0,255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
            # i = 1;

            # speak(f"Hello {name} you are welcome to our class.")
            takeAttendence(name)
            storeNames(name)

    cv2.imshow("video", img)
    print(f"present {names}")
    cv2.waitKey(1000)


print('The End')
