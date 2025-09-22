from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import logging
from .utils import _user_payload, _user_permissions
from ..validators import validate_login_data
from apps.accounts.models import User
from apps.rbac.models import Group, Permission, UserGroup, GroupPermission

logger = logging.getLogger(__name__)

# Serializers for accounts
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username for authentication")
    password = serializers.CharField(help_text="Password for authentication", write_only=True)

class LoginResponseSerializer(serializers.Serializer):
    ok = serializers.BooleanField(help_text="Login success status")
    user = serializers.DictField(help_text="User information", required=False)
    error = serializers.CharField(help_text="Error message", required=False)
    warnings = serializers.ListField(help_text="Validation warnings", required=False)

@swagger_auto_schema(
    method='get',
    operation_description="Get CSRF token for session-based authentication",
    responses={
        200: openapi.Response(
            description="CSRF token retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'csrfToken': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Web Authentication']
)
@require_GET
@ensure_csrf_cookie
def csrf(request):
    """
    Returns a CSRF token and sets the csrftoken cookie.
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


@swagger_auto_schema(
    method='post',
    operation_description="Web login endpoint for session-based authentication",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Login successful",
            schema=LoginResponseSerializer
        ),
        400: openapi.Response(
            description="Bad request - invalid JSON or validation failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                    'details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    'warnings': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            )
        ),
        401: openapi.Response(
            description="Invalid credentials",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Web Authentication']
)
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


@swagger_auto_schema(
    method='post',
    operation_description="Logout from web session",
    responses={
        200: openapi.Response(
            description="Logout successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )
    },
    tags=['Web Authentication']
)
@require_POST
@csrf_protect
def logout(request):
    auth_logout(request)
    return JsonResponse({"ok": True})


@swagger_auto_schema(
    method='get',
    operation_description="Get current authenticated user information",
    responses={
        200: openapi.Response(
            description="User information retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        401: openapi.Response(
            description="User not authenticated",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )
    },
    tags=['Web Authentication']
)
@require_GET
def me(request):
    print(f"Me endpoint called - User authenticated: {request.user.is_authenticated}")
    print(f"Session key: {request.session.session_key}")
    print(f"User: {request.user}")
    
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "user": _user_payload(request.user)})
    return JsonResponse({"authenticated": False}, status=401)