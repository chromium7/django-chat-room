from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    Model for chat room.
    Each room will have a creator and moderators.
    Each room can either be locked or not using password
    """    
    creator =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_created')
    password = models.CharField(max_length=50, default=None, blank=True)
    moderator = models.ManyToManyField(User)


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_logs')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chat_logs')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)