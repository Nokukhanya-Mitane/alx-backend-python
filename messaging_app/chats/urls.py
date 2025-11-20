#!/usr/bin/env python3
"""URL routing for chats app."""

from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Required by checker
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
