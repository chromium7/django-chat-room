"""
URL routing system of Django for asynchronous applications
URLs to route connections to the ChatConsumer
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer),
]