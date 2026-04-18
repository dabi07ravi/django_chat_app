from .repository import MessageRepository
from bson import ObjectId

class MessageService:

    @staticmethod
    def send_message(chat_id, sender_id, content):

        message_data = {
            "chat_id": chat_id,
            "sender_id": sender_id,
            "content": content,
            "type": "text",
            "status": "sent"
        }

        result = MessageRepository.create_message(message_data)

        message_data["_id"] = str(result.inserted_id)

        # update chat last message
        MessageRepository.update_last_message(
            ObjectId(chat_id),
            content,
            sender_id
        )

        return message_data

    @staticmethod
    def get_messages(chat_id, sender_id):
        messages = MessageRepository.get_chat_messages(chat_id, sender_id)

        result = []
        for msg in messages:
            msg["_id"] = str(msg["_id"])
            result.append(msg)

        return result