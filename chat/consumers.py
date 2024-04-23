import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async

from .models import Room, Messages


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.send_all_messages(self.room_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.save_message(message)

        #! Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        # ? type : chat.message pastdagi chat_message ga yo'l ko'rsatadi;
        # ? message : message esa pastdagi funksiyadagi eventga boradi

    async def chat_message(self, event):
        message = event["message"]
        #! Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @sync_to_async
    def send_all_messages(self, event):
        messages = Messages.objects.filter(room__name=event)
        for msg in messages:
            self.send(text_data=json.dumps({"message": msg.message}))

    @sync_to_async
    def save_message(self, event):
        try:
            room = Room.objects.get(name=self.room_name)
        except:
            room = Room.objects.create(name=self.room_name)
        Messages.objects.create(room=room, message=event)
