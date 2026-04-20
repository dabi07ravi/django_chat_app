from .repository import ChatRepository
from datetime import datetime


class ChatService:

    @staticmethod
    def create_or_get_chat(sender_id, receiver_id):

        # check if already exists
        existing = ChatRepository.find_private_chat(sender_id, receiver_id)
        if existing:
            existing["_id"] = str(existing["_id"])  # ✅ fix
            return existing

        # create new chat
        chat_data = {
            "type": "private",
            "participants": [sender_id, receiver_id],
            "last_message": "",
        }

        result = ChatRepository.create_chat(chat_data)
        chat_data["_id"] = str(result.inserted_id)

        return chat_data

    @staticmethod
    def get_user_chats(sender_id):
        chats = ChatRepository.get_user_chats(sender_id)

        chat_list = []
        for chat in chats:
            chat["_id"] = str(chat["_id"])
            chat_list.append(chat)

        return chat_list

    @staticmethod
    def create_group(admin_id, users, name):

        if admin_id not in users:
            users.append(admin_id)

        chat_data = {
            "type": "group",
            "participants": users,
            "name": name,
            "admin_ids": [admin_id],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = ChatRepository.create_chat(chat_data)
        chat_data["_id"] = str(result.inserted_id)

        return chat_data

    @staticmethod
    def add_member(chat_id, admin_id, new_user_id):

        chat = ChatRepository.get_chat_by_id(chat_id)

        if not chat:
            raise Exception("Chat not found")

        if chat["type"] != "group":
            raise Exception("Not a group chat")

        # ✅ Only admin can add
        if admin_id not in chat.get("admin_ids", []):
            raise Exception("Only admin can add members")
        ChatRepository.add_member(chat_id, new_user_id)

        return {"message": "User added successfully"}

    @staticmethod
    def remove_member(chat_id, admin_id, remove_user_id):

        chat = ChatRepository.get_chat_by_id(chat_id)

        if not chat:
            raise Exception("Chat not found")

        if chat["type"] != "group":
            raise Exception("Not a group chat")

        # ✅ Only admin can remove
        if admin_id not in chat.get("admin_ids", []):
            raise Exception("Only admin can remove members")

        # ❗ Optional: prevent removing admin itself
        if remove_user_id in chat.get("admin_ids", []):
            raise Exception("Cannot remove admin")

        removed = ChatRepository.remove_member(chat_id, remove_user_id)


        if removed.matched_count == 0:
            return {"error": "Chat not found"}

        if removed.modified_count == 0:
            return {"error": "User not in chat"}

        return {"message": "User removed successfully"}
