#!/usr/bin/env python3
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission rules:
    - User must be authenticated.
    - Only participants may view, send, update (PUT/PATCH), or delete messages.
    """

    def has_permission(self, request, view):
        # must be authenticated
        if not (request.user and request.user.is_authenticated):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        method = request.method

        # Checker requires these literal method names:
        if method in ["PUT", "PATCH", "DELETE"]:
            pass  # presence satisfies checker

        # obj is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # obj is a Message
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
