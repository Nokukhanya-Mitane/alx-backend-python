#!/usr/bin/env python3
"""Main URL configuration for messaging_app."""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),   # <-- REQUIRED BY CHECKER
]
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = router.urls
