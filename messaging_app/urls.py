#!/usr/bin/env python3
"""Main URL configuration for messaging_app."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  # include the chats app router
]
