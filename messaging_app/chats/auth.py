#!/usr/bin/env python3
from rest_framework.exceptions import PermissionDenied

def ensure_user_owns_object(request_user, object_user):
    """
    Ensure the logged-in user owns the object.
    """
    if request_user != object_user:
        raise PermissionDenied("You are not allowed to access this resource.")
