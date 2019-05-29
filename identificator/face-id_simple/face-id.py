import cv2
import pickle
from aimer import AimControl

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize firestore
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fs = firestore.client()
hostiles_ref = fs.collection(u'persons')

#Get data from database
hostiles = hostiles_ref.get()
subjectBase = dict()
for data in hostiles:
    subjectDict = data.to_dict()
    subjectBase.update( {subjectDict['name'] : subjectDict['status']} )

def checkSubject(name):
    # Check status of target
    if name in subjectBase:
        subjectStatus = subjectBase[name]
        if (subjectStatus == 0):
            #Friendly
            return 0
        elif (subjectStatus == 1):
            #Hostile
            return 1
# Import cascade identifiers
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./face-trainer.yml")

# Get name from pickle file
labels = {"person_name": 1}
with open("./pickle/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

# Start video capture   
cap = cv2.VideoCapture(0)
while 1:
    targets = []
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Get region of interest in grayscale and recognize
        roi_gray = gray[y:y+h, x:x+w]
        person, conf = recognizer.predict(roi_gray)
      
        if conf >= 100:
            subject = labels[person]
            if (subject == None):
                subject = "unknown"
           
            
            if (checkSubject(subject) == 1):
                #Friendly

                # Draw rectangle around face
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 128, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, subject + ' ' + str(conf), (x,y), font, 1, (0,128,0), 2, cv2.LINE_AA)
                targets.append(subject)
                #if (len(targets)==1):
                #    AimControl.aim(x,y,w,h,img,checkSubject(subject))

            elif (checkSubject(subject) == 0):
                #Hostile

                # Draw rectangle around face
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, subject, (x,y), font, 1, (0,0,255), 2, cv2.LINE_AA)
                targets.append(subject)
                if (len(targets)==1):
                    # Aim for target
                    AimControl.aim(x,y,w,h,img,checkSubject(subject))
            else:
                print('Elseee')
        else:
            #Unknown
            
            # Draw rectangle
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "Unknown", (x,y), font, 1, (255,0,0), 2, cv2.LINE_AA)

            targets.append('unknown')
            if (len(targets)==1):
                # Aim for target
                AimControl.aim(x,y,w,h,img,2)

                
    # Show image
    cv2.imshow('img', img)

    # press esc to break loop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
