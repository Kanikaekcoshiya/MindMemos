import bcrypt
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["mindmemosDB"]
users_collection = db["users"]

#AUTH FUNCTIONS 

def hash_password(password: str) -> bytes:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    """Check password against stored hash"""
    return bcrypt.checkpw(password.encode(), hashed)

def add_user(username: str, password: str) -> bool:
    """Create a new user if username doesn't exist"""
    if users_collection.find_one({"username": username}):
        return False
    users_collection.insert_one({
        "username": username,
        "password": hash_password(password)
    })
    return True

def login_user(username: str, password: str) -> bool:
    """Login user by checking credentials"""
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user["password"]):
        return True
    return False
