import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv
load_dotenv()
cred = credentials.Certificate(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
firebase_admin.initialize_app(cred, {"projectId": os.getenv("FIREBASE_PROJECT_ID")})
db = firestore.client()
#test
def verify_firebase_token(id_token: str):
    decoded = auth.verify_id_token(id_token)
    return decoded  # contains uid, email, etc.

def check_and_deduct_credit(uid: str):
    user_ref = db.collection("users").document(uid)
    doc = user_ref.get()
    if not doc.exists:
        user_ref.set({"credits": 1})
        return 1
    credits = doc.to_dict().get("credits", 0)
    if credits < 1:
        raise Exception("No credits")
    user_ref.update({"credits": credits - 1})
    return credits - 1