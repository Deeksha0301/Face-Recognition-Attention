import os
import pickle
import face_recognition
import numpy as np
import cvzone
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred,{
    'databaseURL': '',
    'storageBucket': ""
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for modePath in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, modePath)))

# load the encoding file
print('Loading encode file..')
file = open('EncodeGen.p', 'rb')
encodingsWithIds = pickle.load(file)
file.close()
encodings, studentId = encodingsWithIds
# print(studentId)
print('Encode file loaded..')


modetye = 0
cnt = 0
id = -1
imagStudent = []

while True:
    success, img = cap.read()

    imageS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imageS = cv2.cvtColor(imageS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imageS)
    encodeCurrFrame = face_recognition.face_encodings(imageS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetye]

    if faceCurFrame:
        for encodeFace, faceloca in zip(encodeCurrFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodings, encodeFace)
            faceDis = face_recognition.face_distance(encodings, encodeFace)
            # print("matches", matches)
            # print("face distance", faceDis)

            matchIndex = np.argmin(faceDis)
            # print(matchIndex)

            if matches[matchIndex]:
                # print('Match found!')
                # print(studentId[matchIndex])
                y1, x2, y2, x1 = faceloca
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                id = studentId[matchIndex]
                if cnt == 0:
                    cvzone.putTextRect(imgBackground, 'Loading', (275, 400))
                    cv2.imshow('imgBackground', imgBackground)
                    cv2.waitKey(1)
                    cnt = 1
                    modetye = 1


        if cnt != 0:

            if cnt == 1:
                studentinfo = db.reference(f'Students/{id}').get()
                # print(studentinfo)


                # get the image
                blob = bucket.get_blob(f'Images/{id}.png')
                arr = np.frombuffer(blob.download_as_string(), dtype=np.uint8)
                imgStudent = cv2.imdecode(arr, cv2.COLOR_BGRA2BGR)

                # Update data
                datetimeO = datetime.strptime(studentinfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElp = (datetime.now() - datetimeO).total_seconds()
                print(secondsElp)
                if secondsElp > 30:
                    ref = db.reference(f'Students/{id}')
                    studentinfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentinfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modetye = 3
                    cnt = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetye]


            if modetye != 3:

                if 10 < cnt < 20:
                    modetye = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetye]

                if cnt <= 10:
                    (w, h), _ = cv2.getTextSize(studentinfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2

                    cv2.putText(imgBackground, str(studentinfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentinfo['name']),(808 + offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    cv2.putText(imgBackground, str(studentinfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground, str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentinfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground, str(studentinfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground, str(studentinfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                    imgBackground[175:175+216, 909:909+216] = imgStudent

                cnt += 1

                if cnt >= 20:
                    cnt = 0
                    modetye = 0
                    studentinfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetye]

    else:
        modetye = 0
        cnt = 0

    # cv2.imshow('img', img)
    cv2.imshow('imgBackground', imgBackground)
    cv2.waitKey(1)
