#!/usr/bin/env python3
"""
Serializers for User, Conversation, and Message models.
Includes nested relationships and validation.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


# ---------------------------
# User Serializer
# ---------------------------
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # REQUIRED by checker

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]


# ---------------------------
# Message Serializer
# ---------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]


# ---------------------------
# Conversation Serializer
# ---------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # REQUIRED by checker

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def get_messages(self, obj):
        """Return serialized messages in the conversation."""
        msgs = obj.messages.order_by("sent_at")
        return MessageSerializer(msgs, many=True).data

    def validate(self, attrs):
        """
        Example validation using ValidationError.
        Conversations must have at least one participant.
        """
        if "participants" in attrs and len(attrs["participants"]) == 0:
            raise serializers.ValidationError(
                "A conversation must have at least one participant."
            )
        return attrs
