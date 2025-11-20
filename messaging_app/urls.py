#!/usr/bin/env python3
"""Main URL configuration for messaging_app."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Required by checker: include chats routes under /api/
    path('api/', include('chats.urls')),
]

