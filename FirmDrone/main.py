import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("ressources/key.json")
config = {
    "apiKey": "AIzaSyB8i40Npn45XsjWQnrRY4RbaAEXvlYam2s",
    "authDomain": "imercy-easydrone.firebaseapp.com",
    "databaseURL": "https://imercy-easydrone.firebaseio.com",
    "projectId": "imercy-easydrone",
    "storageBucket": "imercy-easydrone.appspot.com",
    "messagingSenderId": "303395435795",
    "appId": "1:303395435795:web:980d151dbbf6b88b",
    "serviceAccount": "ressources/key.json"
}

firebase_admin.initialize_app(cred)
fb = pyrebase.initialize_app(config)

key = "1111"
mdp = "123"

db = firestore.client()
st = fb.storage()

st.child("droneFW/1111/fw.html").download("g.html")
doc = db.collection(u'drone').document(key)

data = doc.get()
print(doc)
print(format(data.to_dict()))
print(format(data.to_dict()['version']))