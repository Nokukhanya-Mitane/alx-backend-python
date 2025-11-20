#!/usr/bin/env python3
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 JWT Authentication
    path("api/auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Messaging App Routes
    path("api/", include("chats.urls")),

    # DRF Auth (needed for browsable API)
    path("api-auth/", include("rest_framework.urls")),
]

