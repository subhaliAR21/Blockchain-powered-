import pyrebase
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def register(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return "success"
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            return "email_exists"
        print(f"Error: {e}")
        return "failure"

def login(email, password):
    try:
        auth.sign_in_with_email_and_password(email, password)
        return "success"
    except Exception as e:
        error_str = str(e)
        print(f"Login error: {error_str}")
        if "INVALID_PASSWORD" in error_str:
            return "invalid_password"
        elif "EMAIL_NOT_FOUND" in error_str:
            return "email_not_found"
        return "failure"
