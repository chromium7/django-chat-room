'''
Consumers are the equivalent of Django views for asynchronous applications.
Consumers handle WebSockets in a similar way to how traditional views handle HTTP requests.
Consumers are ASGI applications that can handle messages, notifications and other things.
Consumers are built for long running communication.
URLs are mapped to consumers through routing classes that allows combining and stacking consumers.
'''

import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebSocketConsumer):
    def connect(self):
        # Called when a new connection is received
        # Accept connection
        self.accept()

    def disconnect(self, close_code):
        # Called when the socket closes
        # Pass because we dont do any action 
        # when a client closes connection
        pass

    def receive(self, text_data):
        # Called whenever data is received
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Echo the message to WebSocket
        self.send(text_data=json.dumps({'message': message}))

