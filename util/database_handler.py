import uuid

from pymongo import MongoClient
import hashlib
import secrets
import uuid 
from datetime import datetime, timedelta

mongo_client = MongoClient("TeamRocketMongo")
db = mongo_client["TeamRocketDB"] 
user_collection = db["users"]  # database collection containing all users
chat_collection = db["chat"]   # database collection containing all chat messages

#checks if user already exists and adds username + salt + hash into database 
def insert_user(first_name, last_name, email, username, salt, hashedPassword):
    if user_collection.find_one({"username": username}): 
        raise Exception("Username already exists.")
    else:
        user_collection.insert_one({
            "first-name": first_name,
            "last-name": last_name,
            "email": email,
            "username": username,
            "salt": salt,
            "password": hashedPassword,
            "auth_token": ""
            })

def salt_and_hash_password(password):
    salt = secrets.token_hex(16)
    salted_password = password + salt
    salt_hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return salt, salt_hashed_password

def insert_chat_message(username, message_content): 
    message_id = str(uuid.uuid4())
    chat_collection.insert_one({"username": username, "message": message_content, "id": message_id})
    return

def can_earn_coins(username): 
    user = user_collection.find_one({"username": username})
    last_earned = user.get("last_earned")
    if last_earned and (datetime.now() - last_earned) < timedelta(minutes=1):  # 5 minutes cooldown
        return False
    return True

def update_last_earned(username): 
    user_collection.update_one({"username": username}, {"$set": {"last_earned": datetime.now()}})

def add_coins(username, coins): 
    user_collection.update_one({"username": username}, {"$inc": {"coins": coins}})
    return get_user_coins(username)

def get_user_coins(username):
    user = user_collection.find_one({"username": username})
    return user.get("coins", 0)


