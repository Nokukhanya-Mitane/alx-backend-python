#!/usr/bin/env python3
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path."""

    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logging to write into requests.log
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"

        logging.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to chat features outside 6AM–9PM."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access only between 6 AM (06:00) and 9 PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Chat access is restricted between 9PM and 6AM."
            )

        return self.get_response(request)
