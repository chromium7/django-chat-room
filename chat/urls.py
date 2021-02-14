from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.index, name='home'),
    path('chat/', views.chat_redirect, name="chat_redirect"),
    path('chat/create/', views.create_chat_room, name="create_room"),
    path('chat/delete/<int:room_id>/', views.delete_chat_room, name="delete_room"),
    path('chat/<int:room_id>/', views.chat_room, name="chat_room"),
    path('chat/<int:room_id>/leave/', views.leave_chat_room, name="leave_room"),
    path('chat/<int:room_id>/kick/<int:user_id>/', views.kick_user, name="kick_user"),
    path('chat/<int:room_id>/mod/<int:user_id>/', views.mod_user, name="mod_user"),
    path('chat/<int:room_id>/unmod/<int:user_id>/', views.unmod_user, name="unmod_user"),
    
    
]
