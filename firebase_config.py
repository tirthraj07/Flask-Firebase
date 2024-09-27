import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
  'apiKey': os.getenv('FIREBASE_API_KEY'),
  'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
  'projectId': os.getenv('FIREBASE_PROJECT_ID'),
  'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
  'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
  'appId': os.getenv('FIREBASE_APP_ID'),
  'measurementId': os.getenv("FIREBASE_MEASUREMENT_ID"),
  'databaseURL': "" # keep the string empty if real time not used. but the key has to be present
};


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

