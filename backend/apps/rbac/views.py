import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import Role


def _role_payload(role):
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
    }


@require_GET
@csrf_protect
def roles(request):
    """
    Lists all roles.
    """
    roles = Role.objects.all()
    roles_data = [_role_payload(role) for role in roles]
    return JsonResponse({"roles": roles_data})


@require_POST
@csrf_protect
def create_role(request):
    """
    Accepts JSON { "name": str, "description": str }.
    Creates a Role and returns it.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()

    if not name:
        return HttpResponseBadRequest("Role name is required")

    # Prevent duplicate names
    if Role.objects.filter(name=name).exists():
        return JsonResponse({"detail": "Role with this name already exists"}, status=409)

    role = Role.objects.create(name=name, description=description)

    return JsonResponse({"created": True, "role": _role_payload(role)}, status=201)


@require_POST
@csrf_protect
def delete_role(request):
    """
    Accepts query param `role_id`.
    Deletes the Role with the given ID.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
        role_id = data.get("role_id")
    except (json.JSONDecodeError, AttributeError):
        return HttpResponseBadRequest("Invalid JSON")

    if not role_id:
        return HttpResponseBadRequest("role_id is required")

    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return JsonResponse({"detail": "Role not found"}, status=404)

    role.delete()
    return JsonResponse({"deleted": True})




