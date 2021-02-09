from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name='home'),
    path('chat/', views.chat_redirect, name="chat_redirect"),
    path('chat/<int:room_id>/', views.chat_room, name="chat_room"),
]
