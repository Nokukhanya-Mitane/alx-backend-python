#!/usr/bin/env python3
from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Allow access only to users who are part of the conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageSender(permissions.BasePermission):
    """
    Allow sending/editing messages only by the sender.
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
