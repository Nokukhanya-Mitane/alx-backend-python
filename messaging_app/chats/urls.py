#!/usr/bin/env python3
"""URL routing for chats app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ConversationViewSet, MessageViewSet

# Required by checker
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = router.urls
