from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    Model for chat room.
    Each room will have a creator, participants and moderator.
    Each room can either be locked or not using password.
    """
    name = models.CharField(max_length=50)
    creator =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_created')
    participants = models.ManyToManyField(User, related_name='rooms_joined')
    moderators = models.ManyToManyField(User, related_name='rooms_moderated')
    password = models.CharField(max_length=50, default=None, blank=True, null=True)

    def participants_count(self):
        return self.participants.count()

    def moderators_count(self):
        return self.moderators.count()


class Message(models.Model):
    """
    Database model for messages.
    Each message is sent by a user in a room.
    Time will be recorded to be displayed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_logs')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chat_logs')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)