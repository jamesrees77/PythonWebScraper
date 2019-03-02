import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/Users/james/Desktop/WebScraperProject/pythonscraperproject-firebase-adminsdk-2ujy0-749a94c698.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'properties').document()
doc_ref.set({
    u'quote': 'quote'
})

print(quote + 'added to DB')
