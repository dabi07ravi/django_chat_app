from core.db import db
from bson import ObjectId
from datetime import datetime

users_collection = db["users"]

class UserRepository:

    @staticmethod
    def create_user(data):
        data["created_at"] = datetime.utcnow()
        return users_collection.insert_one(data)

    @staticmethod
    def find_by_phone(phone):
        return users_collection.find_one({"phone": phone})

    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def update_user_last_seen(user_id):
        return users_collection.update_one({"_id": ObjectId(user_id)},{"$set": {"last_seen": datetime.utcnow()}})
    
    staticmethod
    def update_profile_pic(user_id, url):
        return users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"profile_pic": url}}
        )