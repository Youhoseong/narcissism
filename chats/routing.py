# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # r"ws/chat/(?P<room_name>\w+)/$" ws/chat/?<string:room_name>/
    # r"ws/chat/(?P<room_name>\w+)/$"
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi())
]
