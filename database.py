import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fs = firestore.client()

hostiles_ref = fs.collection(u'persons')

class FaceDatabase:

    def checkSubject(self, name):
        hostiles = hostiles_ref.get()
        for data in hostiles:
            subject = data.to_dict()
            subjectName = subject['name']
            subjectStatus = subject['status']
            if (subjectName == name):
                if (subjectStatus == 0):
                    print(subjectName)
                    print('hostile')
                    return 1
                elif (subjectStatus == 1):
                    print(subject['name'])
                    print('friendly')
                    return 0