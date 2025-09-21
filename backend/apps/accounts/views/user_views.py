from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .utils import _user_payload
import json
import logging
from ..services.user_services import user_service

logger = logging.getLogger(__name__)


def _parse_json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

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