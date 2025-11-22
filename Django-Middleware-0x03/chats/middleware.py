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



class RolePermissionMiddleware:
    """
    Middleware to enforce user role permissions.
    Only users with roles 'admin' or 'moderator' may access restricted endpoints.
    """

    ALLOWED_ROLES = ["admin", "moderator"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # If user is not authenticated, deny access
        if not user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication required"},
                status=403
            )

        # Attempt to get custom user.role
        user_role = getattr(user, "role", None)

        # Deny if user role is not allowed
        if user_role not in self.ALLOWED_ROLES:
            return JsonResponse(
                {"error": "You do not have permission to perform this action"},
                status=403
            )

        return self.get_response(request)

class RolePermissionMiddleware:
    """
    Middleware to enforce user role permissions.
    Only users with role 'admin' or 'moderator' may continue.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Block if user is not authenticated
        if not user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication required"},
                status=403
            )

        # Get user's role from custom user model
        role = getattr(user, "role", None)

        # Only allow admin or moderator
        if role not in ["admin", "moderator"]:
            return JsonResponse(
                {"error": "Forbidden: insufficient role permissions"},
                status=403
            )

        return self.get_response(request)
