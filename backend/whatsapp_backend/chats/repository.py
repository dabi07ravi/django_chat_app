from core.db import db
from datetime import datetime
from bson import ObjectId


chats_collection = db["chats"]

class ChatRepository:

    @staticmethod
    def find_private_chat(sender_id, receiver_id):
        return chats_collection.find_one({
            "type": "private",
            "participants": {"$all": [sender_id, receiver_id]}
        })

    @staticmethod
    def create_chat(data):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return chats_collection.insert_one(data)

    @staticmethod
    def get_user_chats(sender_id):
        return chats_collection.find({
            "participants": sender_id
        }).sort("updated_at", -1)
    
    @staticmethod
    def get_chat_by_id(chat_id):
        return db["chats"].find_one({"_id": ObjectId(chat_id)})