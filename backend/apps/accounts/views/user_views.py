from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import _user_payload
import json
import logging
from ..services.user_services import user_service

logger = logging.getLogger(__name__)

# Serializers for user management
class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username for the new user")
    email = serializers.EmailField(help_text="Email address")
    password = serializers.CharField(help_text="Password for the user", write_only=True)
    first_name = serializers.CharField(help_text="First name", required=False, allow_blank=True)
    last_name = serializers.CharField(help_text="Last name", required=False, allow_blank=True)
    group = serializers.CharField(help_text="User group (e.g., 'manager', 'admin')", required=False, allow_blank=True)

class UpdateUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="User ID to update")
    username = serializers.CharField(help_text="Username", required=False)
    email = serializers.EmailField(help_text="Email address", required=False)
    password = serializers.CharField(help_text="New password", required=False, write_only=True)
    first_name = serializers.CharField(help_text="First name", required=False, allow_blank=True)
    last_name = serializers.CharField(help_text="Last name", required=False, allow_blank=True)
    group = serializers.CharField(help_text="User group", required=False, allow_blank=True)

class DeleteUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="User ID to delete")

def _parse_json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

@swagger_auto_schema(
    operation_description="Get user(s) - single user by ID or all users (Admin only)",
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="UUID of the user to retrieve (optional)",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID
        )
    ],
    responses={
        200: openapi.Response(
            description="User(s) retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'users': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                }
            )
        ),
        404: openapi.Response(
            description="User not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['User Management'],
    security=[{'Session': []}]
)
@login_required
@require_GET
def users(request, id=None):
    """
    Get user(s) - single user by ID or all users
    """
    if id is not None:
        user = user_service.get_user_by_id(id)
        if not user:
            return JsonResponse({"detail": "User not found"}, status=404)
        return JsonResponse({"user": _user_payload(user)})
    
    users_list = user_service.get_all_users()
    data = [_user_payload(u) for u in users_list]
    return JsonResponse({"users": data})


@swagger_auto_schema(
    operation_description="Create a new user (Admin only)",
    request_body=CreateUserSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'created': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request - invalid data or validation failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        409: openapi.Response(
            description="Conflict - user already exists",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['User Management'],
    security=[{'Session': []}]
)
@login_required
@require_POST
@csrf_protect
def create_user(request):
    """
    Body (JSON):
      {
        "username": str,
        "email": str,
        "password": str,
        "first_name": str?, 
        "last_name": str?,
        "group": str?   # e.g. "manager" or "admin" ...
      }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        logger.warning(f"Invalid JSON in create_user request: {e}")
        return HttpResponseBadRequest(str(e))

    # Use service layer to create user
    success, result = user_service.create_user(data)
    
    if not success:
        error_msg = result.get("error", "Unknown error")
        status_code = 409 if "already exists" in error_msg else 400
        logger.warning(f"User creation failed: {error_msg}")
        return JsonResponse({"detail": error_msg}, status=status_code)

    user = result["user"]
    logger.info(f"User created successfully: {user.username}")
    return JsonResponse({"created": True, "user": _user_payload(user)}, status=201)


@swagger_auto_schema(
    operation_description="Update an existing user (Admin only)",
    request_body=UpdateUserSerializer,
    responses={
        200: openapi.Response(
            description="User updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'updated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request - invalid data or missing ID",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        404: openapi.Response(
            description="User not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        409: openapi.Response(
            description="Conflict - username/email already exists",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['User Management'],
    security=[{'Session': []}]
)
@login_required
@require_POST
@csrf_protect
def update_user(request):
    """
    Body:
      {
        "id": uuid (required),
        "username": str,
        "email": str,
        "password": str,
        "first_name": str?, 
        "last_name": str?,
        "group": str?   # e.g. "manager" or "admin" ...
      }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        logger.warning(f"Invalid JSON in update_user request: {e}")
        return HttpResponseBadRequest(str(e))
 
    user_id = data.get("id")
    if not user_id:
        return HttpResponseBadRequest("id is required")

    # Use service layer to update user
    success, result = user_service.update_user(user_id, data)
    
    if not success:
        error_msg = result.get("error", "Unknown error")
        status_code = 404 if "not found" in error_msg else 409 if "already exists" in error_msg else 400
        logger.warning(f"User update failed: {error_msg}")
        return JsonResponse({"detail": error_msg}, status=status_code)

    user = result["user"]
    logger.info(f"User updated successfully: {user.username}")
    return JsonResponse({"updated": True, "user": _user_payload(user)})


@swagger_auto_schema(
    operation_description="Delete a user (Admin only)",
    request_body=DeleteUserSerializer,
    responses={
        200: openapi.Response(
            description="User deleted successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request - missing ID",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        404: openapi.Response(
            description="User not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['User Management'],
    security=[{'Session': []}]
)
@login_required
@require_POST
@csrf_protect
def delete_user(request):
    """
    Body: { "id": uuid }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        logger.warning(f"Invalid JSON in delete_user request: {e}")
        return HttpResponseBadRequest(str(e))

    user_id = data.get("id")
    if not user_id:
        return HttpResponseBadRequest("id is required")

    # Use service layer to delete user
    success, result = user_service.delete_user(user_id)
    
    if not success:
        error_msg = result.get("error", "Unknown error")
        status_code = 404 if "not found" in error_msg else 400
        logger.warning(f"User deletion failed: {error_msg}")
        return JsonResponse({"detail": error_msg}, status=status_code)

    logger.info(f"User deleted successfully: {user_id}")
    return JsonResponse({"deleted": True})