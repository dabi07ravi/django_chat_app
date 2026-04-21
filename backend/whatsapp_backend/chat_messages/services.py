from .repository import MessageRepository
from bson import ObjectId
import math


class MessageService:

    @staticmethod
    def send_message(chat_id, sender_id, content):

        message_data = {
            "chat_id": chat_id,
            "sender_id": sender_id,
            "content": content,
            "type": "text",
            "status": "sent",
        }

        result = MessageRepository.create_message(message_data)

        message_data["_id"] = str(result.inserted_id)

        # update chat last message
        MessageRepository.update_last_message(ObjectId(chat_id), content, sender_id)

        return message_data

    @staticmethod
    def get_messages(chat_id, sender_id, page, limit):
        messages, total = MessageRepository.get_chat_messages(
            chat_id, sender_id, page, limit
        )

        result = []
        for msg in messages:
            msg["_id"] = str(msg["_id"])
            result.append(msg)

        total_pages = math.ceil(total / limit)

        return {
            "data": result,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "limit": limit,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }
