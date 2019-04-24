# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
from aimer import AimControl

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fs = firestore.client()
hostiles_ref = fs.collection(u'persons')

#Get subjects
hostiles = hostiles_ref.get()
subjectBase = dict()
for data in hostiles:
    subjectDict = data.to_dict()
    subjectBase.update( {subjectDict['name'] : subjectDict['status']} )

def checkSubject(name):
    if name in subjectBase:
        subjectStatus = subjectBase[name]
        if (subjectStatus == 0):
            #Friendly
            return 0
        elif (subjectStatus == 1):
            #Hostile
            return 1
    else:
        return 2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# load the input image and convert it from BGR to RGB
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb,
	model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
names = []

# loop over the facial embeddings
for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
	matches = face_recognition.compare_faces(data["encodings"],
		encoding)
	name = "Unknown"

	# check to see if we have found a match
	if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
		matchedIdxs = [i for (i, b) in enumerate(matches) if b]
		counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face face
		for i in matchedIdxs:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
		name = max(counts, key=counts.get)
	
	# update the list of names
	names.append(name)

# loop over the recognized faces
for ((y, right, bottom, x), name) in zip(boxes, names):
	# draw the predicted face name on the image
		if (checkSubject(name) == 0):
			#Friendly
			AimControl.aim(x,y,(right-x),(bottom-y), image)
			cv2.rectangle(image, (x, y), (right, bottom), (0, 255, 0), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
		elif (checkSubject(name) == 1):
			#Hostile
			AimControl.aim(x,y,(right-x),(bottom-y), image)
			cv2.rectangle(image, (x, y), (right, bottom), (0, 0, 255), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		else:
			#Unknown
			AimControl.aim(x,y,(right-x),(bottom-y), image)
			cv2.rectangle(image, (x, y), (right, bottom), (255, 0, 0), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

# show the output image
print("[INFO] finished analyzing image")
cv2.imshow("Image", image)
cv2.waitKey(0)