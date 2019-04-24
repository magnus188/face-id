# USAGE
# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output output/jurassic_park_trailer_output.avi --display 0

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
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

# add arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", default="encodings.pickle",
	help="path to serialized db of facial encodings")
ap.add_argument("-c", "--capture_input", type=int, default=0,
	help="video input source")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# load the pickle file
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=args["capture_input"]).start()
time.sleep(2.0)
print("[INFO] camera sensor warmed up")

while True:
	frame = vs.read()
	
	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame, then compute
	# the facial embeddings for each face
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	faces = face_recognition.face_encodings(rgb, boxes)
	names = []

	# loop over the facial embeddings
	for face in faces:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			face)
		name = "Unknown"

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

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
		
		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((y, right, bottom, x), name) in zip(boxes, names):
		# rescale the face coordinates
		y = int(y * r)
		right = int(right * r)
		bottom = int(bottom * r)
		x = int(x * r)

		# draw the predicted face name on the image
		if (checkSubject(name) == 0):
			#Friendly
			AimControl.aim(x,y,(right-x),(bottom-y), frame)
			cv2.rectangle(frame, (x, y), (right, bottom), (0, 255, 0), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
		elif (checkSubject(name) == 1):
			#Hostile
			AimControl.aim(x,y,(right-x),(bottom-y), frame)
			cv2.rectangle(frame, (x, y), (right, bottom), (0, 0, 255), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		else:
			#Unknown
			AimControl.aim(x,y,(right-x),(bottom-y), frame)
			cv2.rectangle(frame, (x, y), (right, bottom), (255, 0, 0), 2)
			y = y - 15 if y - 15 > 15 else y + 15
			cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)


	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
	if key == ord("q"):
			break

print("[INFO] done running task")
cv2.destroyAllWindows()