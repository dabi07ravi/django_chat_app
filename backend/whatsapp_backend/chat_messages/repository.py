from core.db import db
from datetime import datetime

messages_collection = db["messages"]
chats_collection = db["chats"]


class MessageRepository:

    @staticmethod
    def create_message(data):
        data["created_at"] = datetime.utcnow()
        return messages_collection.insert_one(data)

    @staticmethod
    def get_chat_messages(chat_id, sender_id, page, limit):
        skip = (page - 1) * limit
        total = messages_collection.count_documents({"chat_id": chat_id})

        messages = (
            messages_collection.find({"chat_id": chat_id, "sender_id": sender_id})
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

        return list(messages), total

    @staticmethod
    def update_last_message(chat_id, message, sender_id):
        chats_collection.update_one(
            {"_id": chat_id, "sender_id": sender_id},
            {"$set": {"last_message": message, "updated_at": datetime.utcnow()}},
        )
