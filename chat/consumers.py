'''
Consumers are the equivalent of Django views for asynchronous applications.
Consumers handle WebSockets in a similar way to how traditional views handle HTTP requests.
Consumers are ASGI applications that can handle messages, notifications and other things.
Consumers are built for long running communication.
URLs are mapped to consumers through routing classes that allows combining and stacking consumers.
'''

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called when a new connection is received
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.id
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # Called when the socket closes
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Called whenever data is received
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # Send the message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))