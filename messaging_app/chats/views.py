#!/usr/bin/env python3
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # Add filtering + pagination
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        # required for django_filters
        django_filters.rest_framework.DjangoFilterBackend,
    ]

    search_fields = ["message_body"]
    ordering_fields = ["sent_at"]

    def get_queryset(self):
        """
        Only show messages in conversations that the user belongs to.
        """
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """
        Users can only send messages in conversations they participate in.
        """
        conversation_id = self.request.data.get("conversation_id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if self.request.user not in conversation.participants.all():
            return Response(
                {"error": "Not allowed"},
                status=HTTP_403_FORBIDDEN,
            )

        serializer.save(sender=self.request.user, conversation=conversation)
