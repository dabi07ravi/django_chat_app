import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_messages.services import MessageService
from asgiref.sync import sync_to_async
import traceback
from chats.repository import ChatRepository
import asyncio




class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user_id = self.scope.get("user_id")

        await self.accept()   # ✅ MUST DO FIRST

        if not self.user_id:
            await self.send(json.dumps({"error": "Unauthorized"}))
            await self.close()
            return

        chat = await sync_to_async(ChatRepository.get_chat_by_id)(self.chat_id)
        if not chat:
            print("❌ Chat not found triggered")
            await self.send(json.dumps({"error": "Chat not found"}))
            await self.close()
            return

        if str(self.user_id) not in [str(p) for p in chat["participants"]]:
            await self.send(json.dumps({"error": "Access denied"}))
            await self.close()
            return

        self.room_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            content = data['content']

            message = MessageService.send_message(
                self.chat_id,
                self.user_id,
                content
            )

            if "created_at" in message:
                message["created_at"] = message["created_at"].isoformat()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                'type': 'chat_message',
                'message': message
                 }
            )

        except Exception as e:
            traceback.print_exc()   # 🔥 IMPORTANT


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))