import pickle
import cv2
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred,{
    'databaseURL': '',
    'storageBucket': ""
})


# importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []

studentId = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(os.path.splitext(path)[0])
    studentId.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


# print(imgList)

def encodeGen(imList):
    # print("Encoding")
    enco = []
    for image in imList:
        # print("Encoding")
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            enco.append(encode)
            # print(enco)
        except IndexError:
            # Handle the case where no face is found in the image
            print("No face found in an image.")
            encodings.append(None)
    return enco


print('start')
encodings = encodeGen(imgList)
encodingsWithIds = [encodings, studentId]
print('end')

file = open('EncodeGen.p', 'wb')
pickle.dump(encodingsWithIds, file)
file.close()
print('done')
