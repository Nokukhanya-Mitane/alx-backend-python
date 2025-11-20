#!/usr/bin/env python3
from django.db import models

#!/usr/bin/env python3
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ---------------------------
# Custom User Model
# ---------------------------
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds fields required by project specification.
    """
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    # Django already provides:
    # username, first_name, last_name, email, password, etc.

    def __str__(self):
        return f"{self.username} ({self.email})"


# ---------------------------
# Conversation Model
# ---------------------------
class Conversation(models.Model):
    """
    Tracks a conversation between multiple users.
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ---------------------------
# Message Model
# ---------------------------
class Message(models.Model):
    """
    Message sent within a conversation.
    """
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
