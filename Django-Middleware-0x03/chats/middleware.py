#!/usr/bin/env python3
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse


class RequestLoggingMiddleware:
    """
    Middleware that logs user requests with timestamp, user and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Restricts access outside 6PM - 9PM
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is restricted at this time.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Limits POST requests to 5 per minute per IP.
    """

    ip_requests = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            now = datetime.now()

            self.ip_requests.setdefault(ip, [])
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip]
                if (now - t).seconds < 60
            ]

            if len(self.ip_requests[ip]) >= 5:
                return JsonResponse(
                    {"error": "Too many messages sent. Try again later."},
                    status=429
                )

            self.ip_requests[ip].append(now)

        return self.get_response(request)


class RolepermissionMiddleware:
    """
    Allows only admin or moderator users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("Authentication required")

        role = getattr(user, "role", None)

        if role not in ["admin", "moderator"]:
            return HttpResponseForbidden("Access denied")

        return self.get_response(request)
