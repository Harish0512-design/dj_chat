import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # join the room
        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # leave the group
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )

    # receive message from websocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data["message"]

        # send message to room
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat.message",
                "message": message
            }
        )

    # receive message from room
    async def chat_message(self, event):
        message = event["message"]

        # send message to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message
                }
            )
        )
