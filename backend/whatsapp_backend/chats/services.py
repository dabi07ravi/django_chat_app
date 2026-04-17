from .repository import ChatRepository

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
            "last_message": ""
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