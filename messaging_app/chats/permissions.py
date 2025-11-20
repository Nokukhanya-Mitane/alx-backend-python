#!/usr/bin/env python3
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - User must be authenticated
    - User can only access conversations they participate in
    - User can only access messages in conversations they belong to
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj may be:
        - Conversation → check participants
        - Message → check message.conversation.participants
        """

        # If object is a conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If object is a message → use its conversation
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
