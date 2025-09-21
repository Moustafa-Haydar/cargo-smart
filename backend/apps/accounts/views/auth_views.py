from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
import json
import logging
from .utils import _user_payload, _user_permissions
from ..validators import validate_login_data
from apps.accounts.models import User
from apps.rbac.models import Group, Permission, UserGroup, GroupPermission

logger = logging.getLogger(__name__)


@require_GET
@ensure_csrf_cookie
def csrf(request):
    """
    Returns a CSRF token and sets the csrftoken cookie.
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


@require_POST
@csrf_protect
def login(request):
    """
    Body: { "username": str, "password": str }
    Creates a Django session on success.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in login request")
        return JsonResponse({"ok": False, "error": "Invalid JSON format"}, status=400)

    # Validate request data
    is_valid, validation_result = validate_login_data(data, is_mobile=False)
    
    if not is_valid:
        logger.warning(f"Login validation failed: {validation_result.get('errors', [])}")
        return JsonResponse({
            "ok": False, 
            "error": "Validation failed",
            "details": validation_result.get('errors', []),
            "warnings": validation_result.get('warnings', [])
        }, status=400)

    username = validation_result['username']
    password = validation_result['password']
    warnings = validation_result.get('warnings', [])

    # Log security warnings if any
    if warnings:
        logger.warning(f"Login warnings for user {username}: {warnings}")

    user = authenticate(request, username=username, password=password)
    if not user:
        logger.warning(f"Login failed - Invalid credentials for username: {username}")
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)

    logger.info(f"Login successful for user: {user.username}")
    auth_login(request, user)
    logger.info(f"Session created - Session key: {request.session.session_key}")

    # Optional: cache permission ids in session for quick checks (invalidate on group updates)
    perm_ids, _ = _user_permissions(user)
    request.session["permission_ids"] = perm_ids

    response_data = {"ok": True, "user": _user_payload(user)}
    
    # Include warnings in response if any
    if warnings:
        response_data["warnings"] = warnings

    return JsonResponse(response_data)


@require_POST
@csrf_protect
def logout(request):
    auth_logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    print(f"Me endpoint called - User authenticated: {request.user.is_authenticated}")
    print(f"Session key: {request.session.session_key}")
    print(f"User: {request.user}")
    
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "user": _user_payload(request.user)})
    return JsonResponse({"authenticated": False}, status=401)