import cv2
import numpy as np
import face_recognition
import dlib
# load image and convert into RGB

imgShihab = face_recognition.load_image_file('images/Shihab.jpg')
imgShihab = cv2.cvtColor(imgShihab, cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file('images/Shihab_Test.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

faceloc = face_recognition.face_locations(imgShihab)[0]
encodeShihab = face_recognition.face_encodings(imgShihab)[0]
cv2.rectangle(imgShihab, (faceloc[3], faceloc[0]), (faceloc[1], faceloc[2]), (255, 0, 255), 2)
# print(encodeShihab)


facelocTest = face_recognition.face_locations(imgTest)[0]
encodeShihabTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (facelocTest[3], facelocTest[0]), (facelocTest[1], facelocTest[2]), (255, 0, 255), 2)

# Comparing faces
results = face_recognition.compare_faces([encodeShihab], encodeShihabTest)
# measure the distance between the images.lower the distance ,the better the match is
facedis = face_recognition.face_distance([encodeShihab], encodeShihabTest)
print(results, facedis)

cv2.putText(imgTest, f'{results} {round(facedis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 0, 255),2)

cv2.imshow('Shihab', imgShihab)

cv2.imshow('Shihab Test', imgTest)
cv2.waitKey(0)
