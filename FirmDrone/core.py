# Firebase Import
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Json Import
import json

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


# Nexus : Définition des fontions principals
class nexus:
    def __init__(self, key, mdp):
        self.key = key
        self.mdp = mdp
        self.auth = 2

    # checkMDP : Check le mdp et auth
    def checkMDP(self):
        doc = db.collection(u'drone').document(self.key).get()
        if self.mdp == doc.to_dict()['mdpdrone']:
            self.auth = 1
            return self.auth
        else:
            print("[CORE] Erreur pendant le check du Mot de Passe")
            self.auth = 0
            return self.auth

    # getVersion : Permet d'obtenir la version sur la DB
    def getVersion(self):
        doc = db.collection(u'drone').document(self.key).get()
        if self.auth == 1:
            version = doc.to_dict()['version']
            return version

    # getFile : Fonction universelle qui permet d'obtenir un fichier sur Storage et de l'installer dans un
    # emplacement localement
    def getFile(self, path, file):
        if self.auth == 1:
            st.child(path).download(file)
            return True

    # returnKey : Retourne la key entré dans l'init
    def returnKey(self):
        return self.key

    # returnMDP : Retourne le MDP entré dans l'init
    def returnMDP(self):
        return self.mdp


# FW : Gestion du FirmWare Utilisateur du drone
class FW:
    def __init__(self, key, mdp, version):
        self.path = "droneFW/" + key + "/fw.py"
        self.file = "FW_User/fw.py"
        self.version = version
        self.key = key
        self.mdp = mdp

    # getFW : Obtenir le FW si il n'est pas à jour et le mettre dans les fichiers locaux
    def getFW(self):
        if self.version:
            print("[FW] Firmware à jour !")
        else:
            print("[FW] Nouveau FW détecté, téléchargement en cours...")
            n = nexus(self.key, self.mdp)
            n.checkMDP()
            n.getFile(self.path, self.file)
            print("[FW] FW téléchargé !")

    # applyFW : Applique le FW User sur le drone
    def applyFW(self):
        print("In progress")


# manageData : Gestion des données interne du drone
class manageData:
    def __init__(self):
        self.pathConfig = 'ressources/config.json'
        self.pathData = 'ressources/db.json'

    # returnKey : Retourne la key se trouvant dans le fichier JSON
    def returnKey(self):
        with open(self.pathConfig) as f:
            data = json.load(f)
        return data['key']

    # returnMDP : Retourne le mot de passe se trouvant dans le fichier JSON
    def returnMDP(self):
        with open(self.pathConfig) as f:
            data = json.load(f)
        return data['mdp']

    # saveDB : Sauvegarde la base de données dans les fichiers locaux
    def SaveDB(self):
        with open(self.pathConfig) as f:
            key = json.load(f)
        doc = db.collection(u'drone').document(key['key']).get()
        with open(self.pathData, 'w') as outfile:
            json.dump(doc.to_dict(), outfile)

    # writeDB : Ecrit une nouvelle valeur en fonction de la key dans la base de données Internet
    def writeDB(self, k, v):
        with open(self.pathConfig) as f:
            key = json.load(f)
        doc = db.collection(u'drone').document(key['key'])
        doc.update({
            k: v
        })

    # removeDB : Supprime une valeur en fonction de la key de la base de données Internet
    def removeDB(self, k):
        with open(self.pathConfig) as f:
            key = json.load(f)
        doc = db.collection(u'drone').document(key['key'])
        doc.update({
            k: db.DELETE_FIELD
        })

    # compareDB : Compare la valeur de la version local et la valeur de la version internet de la base de données
    def compareDB(self, kone, ktwo):
        with open(self.pathConfig) as f:
            key = json.load(f)
        with open(self.pathData) as f:
            data = json.load(f)
        doc = db.collection(u'drone').document(key['key']).get()
        if doc.to_dict()[kone] == data[ktwo]:
            return True
        else:
            return False

    # compareVersion : Compare la version du FW local et la version du FW sur Internet
    def compareVersion(self):
        with open(self.pathConfig) as f:
            key = json.load(f)
        with open(self.pathData) as f:
            data = json.load(f)
        doc = db.collection(u'drone').document(key['key']).get()
        v = doc.to_dict()['version']
        if v == data['version']:
            return True
        else:
            return False


# security : Gestion de la sécurité du drone
class security:
    def __init__(self):
        self.s = ""

    def VolSecurity(self):
        self.s = 1


# analytics : Gestion des données, de l'analyse et des capteurs
class analytics:
    def __init__(self):
        self.a = ""

    def getStatus(self):
        self.a = 1
