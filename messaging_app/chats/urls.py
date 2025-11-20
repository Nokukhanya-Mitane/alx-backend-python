#!/usr/bin/env python3
"""
URL routing for chats app.
Registers ViewSets for Conversations and Messages.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),
]
