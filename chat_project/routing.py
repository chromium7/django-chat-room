"""
Global routing file
The standard ProtocolTypeRouter automatically maps HTTP requests to
the standard Django views if no specific http mapping is provided
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})