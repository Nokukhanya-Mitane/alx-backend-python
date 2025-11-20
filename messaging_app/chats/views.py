#!/usr/bin/env python3
from django.shortcuts import render

#!/usr/bin/env python3
"""
Viewsets for Conversations and Messages API.
Allows listing, creating conversations, and sending messages.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer,
)

User = get_user_model()


# ---------------------------------------------------------
# Conversation ViewSet
# ---------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Listing a user's conversations
    - Creating a conversation with participants
    - Viewing a conversation's messages
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def list(self, request, *args, **kwargs):
        """List only the conversations the authenticated user is part of."""
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Expected payload:
        {
            "participants": [user_id1, user_id2, ...]
        }
        """
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "Conversation must have at least one participant."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Add requesting user automatically
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, *participants)
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """Return all messages in this conversation."""
        conversation = self.get_object()
        msgs = conversation.messages.order_by("sent_at")
        return Response(MessageSerializer(msgs, many=True).data)


# ---------------------------------------------------------
# Message ViewSet
# ---------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Listing messages
    - Sending a message to a conversation
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        Expected payload:
        {
            "conversation": "<conversation_id>",
            "message_body": "Hello world"
        }
        """
        convo_id = request.data.get("conversation")
        body = request.data.get("message_body")

        if not convo_id or not body:
            return Response(
                {"error": "conversation and message_body fields required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(conversation_id=convo_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=body,
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )
