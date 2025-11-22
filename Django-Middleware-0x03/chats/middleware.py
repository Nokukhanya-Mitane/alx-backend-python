#!/usr/bin/env python3
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse


class OffensiveLanguageMiddleware:
    """
    Middleware to limit message sending per IP address.
    Allows max 5 POST requests per minute.
    """

    # Store IP timestamps: { "ip": [timestamp1, timestamp2, ...] }
    ip_request_log = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only monitor POST requests (sending messages)
        if request.method == "POST":
            now = datetime.now()

            # Initialize list for this IP
            if ip not in self.ip_request_log:
                self.ip_request_log[ip] = []

            # Filter timestamps: keep only messages from the last 60 seconds
            one_minute_ago = now - timedelta(minutes=1)
            self.ip_request_log[ip] = [
                ts for ts in self.ip_request_log[ip] if ts > one_minute_ago
            ]

            # Check if user exceeded limit
            if len(self.ip_request_log[ip]) >= 5:
                return JsonResponse(
                    {
                        "error": "Message rate limit exceeded. Try again in 1 minute."
                    },
                    status=429  # Too Many Requests
                )

            # Add new timestamp
            self.ip_request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve the client IP safely."""
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")



class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # Allow only admin or moderator
        if user and user.is_authenticated:
            role = getattr(user, "role", None)
            if role not in ["admin", "moderator"]:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("Access denied: insufficient role permissions.")

        return self.get_response(request)
