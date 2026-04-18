import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_messages.services import MessageService
from asgiref.sync import sync_to_async
import traceback


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("WebSocket connecting...")  # DEBUG
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"

        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            sender_id = data['sender_id']
            content = data['content']

            message = MessageService.send_message(
                self.chat_id,
                sender_id,
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
            print("❌ ERROR:", str(e))
            traceback.print_exc()   # 🔥 IMPORTANT


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))