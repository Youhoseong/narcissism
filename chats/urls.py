# chat/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    # r"^(?P<room_name>[^/]+)/$"
    path("<str:room_name>/", views.room, name="room"),
]

