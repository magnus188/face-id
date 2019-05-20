import cv2
from aimer import AimControl

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        
        subject = "unknown"
        targets = dict()
        targets.update({
            subject: (x,y,w,h)
        })

        #Unknown
        if (len(targets)==1):
            AimControl.aim(targets,img,2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "Unknown", (x,y), font, 1, (255,0,0), 2, cv2.LINE_AA)       
    
    cv2.imshow('img', img)

    # press esc to break
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
