#!/usr/bin/env python3
from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Main router
router = routers.DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + conversations_router.urls
#!/usr/bin/env python3
"""Main URL routing for messaging_app."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Required for assignment checkers
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
