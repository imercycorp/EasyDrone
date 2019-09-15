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

db = firestore.client()
st = fb.storage()


class nexus:
    def __init__(self, key, mdp):
        self.key = key
        self.mdp = mdp
        self.auth = 2

    def checkMDP(self):
        doc = db.collection(u'drone').document(self.key).get()
        if self.mdp == doc.to_dict()['mdpdrone']:
            self.auth = 1
            return self.auth
        else:
            print("[CORE] Erreur pendant le check du Mot de Passe")
            self.auth = 0
            return

    def getVersion(self):
        doc = db.collection(u'drone').document(self.key).get()
        if self.auth == 1:
            version = doc.to_dict()['version']
            return version

    def getFile(self, path, file):
        if self.auth == 1:
            st.child(path).download(file)
            return True

    def returnKey(self):
        return self.key

    def returnMDP(self):
        return self.mdp


class FW:
    def __init__(self, key, mdp, version, versionDB):
        self.path = "droneFW/"+key+"/fw.py"
        self.file = "FW_User/fw.py"
        self.version = version
        self.versionDB = versionDB
        self.key = key
        self.mdp = mdp

    def getFW(self):
        if self.version == self.versionDB:
            print("[FW] Firmware à jour !")
        else:
            print("[FW] Nouveau FW détecté, téléchargement en cours...")
            n = nexus(self.key, self.mdp)
            n.checkMDP()
            n.getFile(self.path, self.file)
            print("[FW] FW téléchargé !")

    def applyFW(self):
        print("In progress")


class manageData:
    def __init__(self, path):
        self.path = path