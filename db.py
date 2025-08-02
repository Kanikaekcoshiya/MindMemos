from pymongo import MongoClient
from datetime import datetime
import os
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup with certifi for SSL
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = client["mindmemosDB"]
users_collection = db["users"]
history_collection = db["history"]
feedback_collection = db["feedback"]

# ========================== HISTORY FUNCTIONS ==============================
def save_history(username, filename, note_type, language, output):
    """Save processed file history for user"""
    history_collection.insert_one({
        "username": username,
        "filename": filename,
        "note_type": note_type,
        "language": language,
        "output": output,
        "timestamp": datetime.now()
    })

def get_history(username):
    """Fetch user history sorted by latest"""
    return list(history_collection.find({"username": username}).sort("timestamp", -1))

# ========================== FEEDBACK FUNCTIONS ==============================
def save_feedback(username, filename, feedback_text):
    """Save user feedback"""
    feedback_collection.insert_one({
        "username": username,
        "filename": filename,
        "feedback": feedback_text,
        "timestamp": datetime.now()
    })
