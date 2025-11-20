#!/usr/bin/env python3
import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Allow filtering messages by:
    - sender
    - conversation
    - date/time range
    """
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = {
            "sender": ["exact"],
            "conversation": ["exact"],
        }
